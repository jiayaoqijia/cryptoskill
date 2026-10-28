// Read-only original-file mappings and current bytes. No transactions or writes to Program.
// @category DSH.Evidence
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.Function;
import ghidra.file.formats.android.dex.DexHeaderFactory;
import ghidra.file.formats.android.dex.format.*;
import ghidra.file.formats.android.dex.util.DexUtil;
import com.google.gson.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.*;

public class ReEvidenceSnapshot extends GhidraScript {
    private static String hash(byte[] bytes) throws Exception {
        byte[] digest=MessageDigest.getInstance("SHA-256").digest(bytes);
        StringBuilder s=new StringBuilder();for(byte b:digest)s.append(String.format("%02x",b&255));return s.toString();
    }
    private static long integer(JsonObject o,String key) { return Long.decode(o.get(key).getAsString()); }
    private Address dexAddress(JsonObject q) throws Exception {
        // Read the installed loader's actual lookup table via its public API.
        // Never synthesize a Dalvik method PC from a hardcoded base or name.
        DexHeader header=DexHeaderFactory.getDexHeader(currentProgram);
        int index=q.get("dex_method_index").getAsInt();
        if(index<0||index>=header.getMethods().size())throw new IllegalArgumentException("DEX method index outside header");
        MethodIDItem method=header.getMethods().get(index);
        StringBuilder sig=new StringBuilder(DexUtil.convertTypeIndexToString(header,method.getClassIndex()));
        sig.append("->").append(DexUtil.convertToString(header,method.getNameIndex())).append("(");
        PrototypesIDItem proto=header.getPrototypes().get(method.getProtoIndex()&0xffff);
        if(proto.getParameters()!=null)for(TypeItem parameter:proto.getParameters().getItems())sig.append(DexUtil.convertTypeIndexToString(header,parameter.getType()));
        sig.append(")").append(DexUtil.convertTypeIndexToString(header,proto.getReturnTypeIndex()));
        if(!sig.toString().equals(q.get("signature").getAsString()))throw new IllegalArgumentException("Loaded DEX method descriptor differs from indexed original");
        Address lookup=DexUtil.toLookupAddress(currentProgram,index);
        long value=Integer.toUnsignedLong(currentProgram.getMemory().getInt(lookup));
        if(value==0xffffffffL)throw new IllegalArgumentException("DEX method has no initialized lookup entry");
        return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(value);
    }
    public void run() throws Exception {
        String[] args=getScriptArgs();if(args.length!=2)throw new IllegalArgumentException("request.json new-snapshot.json required");
        if(currentProgram==null)throw new IllegalStateException("Open a program first");
        Path output=Paths.get(args[1]).toAbsolutePath();
        if(Files.exists(output)||Files.isSymbolicLink(output))throw new IllegalArgumentException("Snapshot output already exists");
        byte[] requestBytes=Files.readAllBytes(Paths.get(args[0]));
        JsonObject request=JsonParser.parseString(new String(requestBytes,StandardCharsets.UTF_8)).getAsJsonObject();
        if(!"dsh-re-static-request-v1".equals(request.get("schema").getAsString()))throw new IllegalArgumentException("Unknown request schema");
        String sourceHash=currentProgram.getExecutableSHA256();
        if(sourceHash==null||!sourceHash.equalsIgnoreCase(request.get("image_sha256").getAsString()))throw new IllegalArgumentException("Program executable hash differs from requested original file");
        long before=currentProgram.getModificationNumber();
        JsonObject result=new JsonObject();result.addProperty("schema","dsh-re-static-snapshot-v1");
        result.addProperty("request_sha256",hash(requestBytes));result.addProperty("producer_epoch",UUID.randomUUID().toString());
        result.addProperty("program_sha256",sourceHash.toLowerCase());result.addProperty("program_name",currentProgram.getName());
        result.addProperty("language",currentProgram.getLanguageID().toString());result.addProperty("compiler",currentProgram.getCompilerSpec().getCompilerSpecID().toString());
        result.addProperty("space",currentProgram.getAddressFactory().getDefaultAddressSpace().getName());
        result.addProperty("image_base",currentProgram.getImageBase().toString());
        JsonArray rows=new JsonArray();
        long budget=request.has("read_byte_budget")?request.get("read_byte_budget").getAsLong():8388608L;
        if(budget<1)throw new IllegalArgumentException("Positive per-query byte budget required");
        for(JsonElement element:request.getAsJsonArray("queries")) {
            monitor.checkCancelled();JsonObject q=element.getAsJsonObject();JsonObject row=new JsonObject();
            row.addProperty("key",q.get("key").getAsString());row.add("file_offset_bytes",q.get("file_offset_bytes"));
            long offset=integer(q,"file_offset_bytes"),length=q.get("bytes").getAsLong();
            if(offset<0||length<1)throw new IllegalArgumentException("Invalid requested file span");
            JsonArray matches=new JsonArray();row.add("matches",matches);
            if(length>budget||length>Integer.MAX_VALUE) { row.addProperty("state","not_read_budget");rows.add(row);continue; }
            List<Address> addresses;
            try {
                if("dex".equals(request.get("kind").getAsString())) {
                    addresses=Collections.singletonList(dexAddress(q));row.addProperty("mapping_basis","loaded_dalvik_descriptor_and_method_lookup");
                } else {
                    addresses=currentProgram.getMemory().locateAddressesForFileOffset(offset);row.addProperty("mapping_basis","ghidra_filebytes_mapping");
                }
            } catch(Exception e) { row.addProperty("state","mapping_unavailable");row.addProperty("error",e.toString());rows.add(row);continue; }
            for(Address address:addresses) {
                JsonObject match=new JsonObject();match.addProperty("address",address.toString());match.addProperty("space",address.getAddressSpace().getName());
                try {
                    byte[] bytes=new byte[(int)length];int count=currentProgram.getMemory().getBytes(address,bytes);
                    if(count!=length)throw new IllegalStateException("Short memory read");
                    String digest=hash(bytes);match.addProperty("bytes",count);match.addProperty("bytes_sha256",digest);match.addProperty("bytes_match",digest.equals(q.get("sha256").getAsString()));
                    Function function=currentProgram.getFunctionManager().getFunctionContaining(address);
                    if(function!=null) {
                        JsonObject f=new JsonObject();f.addProperty("name",function.getName(true));f.addProperty("entry",function.getEntryPoint().toString());
                        f.addProperty("prototype",function.getPrototypeString(true,true));JsonArray ranges=new JsonArray();
                        for(AddressRange range:function.getBody().getAddressRanges()) {
                            JsonObject r=new JsonObject();r.addProperty("space",range.getMinAddress().getAddressSpace().getName());
                            r.addProperty("start",range.getMinAddress().toString());r.addProperty("end",range.getMaxAddress().toString());ranges.add(r);
                        }
                        f.add("body_ranges",ranges);match.add("function",f);
                    }
                    match.addProperty("state","read");
                } catch(Exception e) { match.addProperty("state","read_failed");match.addProperty("error",e.toString()); }
                matches.add(match);
            }
            row.addProperty("state",matches.size()==0?"unmapped":"candidates");rows.add(row);
        }
        result.add("queries",rows);long after=currentProgram.getModificationNumber();
        if(before!=after)throw new IllegalStateException("Program changed during snapshot; no artifact published");
        result.addProperty("program_modification_before",Long.toString(before));result.addProperty("program_modification_after",Long.toString(after));
        result.addProperty("program_unchanged",true);result.addProperty("authority","current original-file mappings and queried bytes; no runtime identity or semantic acceptance proof");
        Files.createDirectories(output.getParent());Path temp=Files.createTempFile(output.getParent(),".re-static-",".json");
        try { Files.write(temp,new GsonBuilder().disableHtmlEscaping().create().toJson(result).getBytes(StandardCharsets.UTF_8));Files.createLink(output,temp); }
        finally { Files.deleteIfExists(temp); }
        println("Read-only evidence snapshot: "+output);
    }
}
