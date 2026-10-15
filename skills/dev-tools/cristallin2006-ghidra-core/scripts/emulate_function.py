# Ghidra script to emulate function execution using P-code emulator
# @category DSH.Reverse
# @runtime PyGhidra

# --- DSH @out support (self-contained, no cross-script imports) ---
# If the first script argument starts with '@', it is popped and treated as an
# output file path: the full JSON payload is written there, and stdout only
# carries a short status summary between the markers.
_DSH_OUT_PATH = None

def _dsh_extract_out():
    global _DSH_OUT_PATH
    try:
        args = list(getScriptArgs())
    except NameError:
        return []
    if args and str(args[0]).startswith("@"):
        _DSH_OUT_PATH = str(args[0])[1:]
        args = args[1:]
    return args

_DSH_ARGS = _dsh_extract_out()
# --- end DSH @out support ---


import json
from ghidra.app.emulator import EmulatorHelper
from ghidra.program.model.address import AddressSet
from ghidra.program.model.listing import CodeUnit
from ghidra.util.task import ConsoleTaskMonitor

def output_json(data):
    """Write full JSON to the @out file if given, else print between markers."""
    if _DSH_OUT_PATH:
        try:
            f = open(_DSH_OUT_PATH, "w")
            try:
                f.write(json.dumps(data))
            finally:
                f.close()
            count = 0
            for key in ("strings", "functions", "instructions", "results",
                        "imports", "symbols", "xrefs", "blocks", "classes",
                        "basic_blocks", "c_code", "bytes"):
                if key in data and data[key] is not None:
                    v = data[key]
                    try:
                        count = len(v)
                    except TypeError:
                        count = 1
                    break
            if "string_count" in data:
                count = data["string_count"]
            elif "function_count" in data:
                count = data["function_count"]
            elif "instruction_count" in data:
                count = data["instruction_count"]
            summary = {
                "status": data.get("status", "success"),
                "out": _DSH_OUT_PATH,
                "count": count
            }
            if data.get("status") == "error":
                summary["error"] = data.get("error")
            print("===JSON_START===")
            print(json.dumps(summary))
            print("===JSON_END===")
        except Exception as write_err:
            print("===JSON_START===")
            print(json.dumps({"status": "error",
                              "error": "failed to write out file: " + str(write_err)}))
            print("===JSON_END===")
    else:
        print("===JSON_START===")
        print(json.dumps(data))
        print("===JSON_END===")

def find_function(program, identifier):
    """Find a function by name or address."""
    fm = program.getFunctionManager()

    if identifier.startswith("0x") or identifier.startswith("0X"):
        try:
            addr = toAddr(identifier)
            func = fm.getFunctionAt(addr)
            if func:
                return func
            func = fm.getFunctionContaining(addr)
            if func:
                return func
        except:
            pass

    for func in fm.getFunctions(True):
        if func.getName() == identifier:
            return func

    for func in fm.getFunctions(True):
        if identifier.lower() in func.getName().lower():
            return func

    return None

def parse_register_inputs(inputs_str):
    """Parse register inputs from JSON string."""
    if not inputs_str:
        return {}
    try:
        return json.loads(inputs_str)
    except:
        return {}

def parse_memory_inputs(memory_str):
    """Parse memory inputs from JSON string."""
    if not memory_str:
        return {}
    try:
        return json.loads(memory_str)
    except:
        return {}

def run():
    """Main script entry point."""
    try:
        program = currentProgram
        if program is None:
            output_json({"status": "error", "error": "No program loaded"})
            return

        args = _DSH_ARGS
        if not args:
            output_json({
                "status": "error",
                "error": "Usage: <function_name|address> [register_inputs_json] [memory_inputs_json] [max_steps]"
            })
            return

        func_identifier = args[0]
        register_inputs_str = args[1] if len(args) > 1 else "{}"
        memory_inputs_str = args[2] if len(args) > 2 else "{}"
        max_steps = int(args[3]) if len(args) > 3 else 10000

        # Find the function
        func = find_function(program, func_identifier)
        if func is None:
            output_json({
                "status": "error",
                "error": "Function not found: " + func_identifier
            })
            return

        # Parse inputs
        register_inputs = parse_register_inputs(register_inputs_str)
        memory_inputs = parse_memory_inputs(memory_inputs_str)

        # Create emulator helper
        emulator = EmulatorHelper(program)
        monitor = ConsoleTaskMonitor()

        try:
            # Get function entry point
            entry_point = func.getEntryPoint()

            # Set up register inputs
            skipped_inputs = []
            for reg_name, value in register_inputs.items():
                try:
                    reg = emulator.getLanguage().getRegister(reg_name)
                    if reg is None:
                        raise ValueError("unknown register: " + str(reg_name))
                    # Convert value to int
                    if isinstance(value, str):
                        if value.startswith("0x") or value.startswith("0X"):
                            value = int(value, 16)
                        else:
                            value = int(value)
                    emulator.writeRegister(reg, value)
                except Exception as e:
                    skipped_inputs.append({
                        "kind": "register", "name": str(reg_name),
                        "value": value if isinstance(value, (int, str)) else str(value),
                        "reason": str(e)
                    })

            # Set up memory inputs
            for addr_str, data in memory_inputs.items():
                try:
                    addr = toAddr(addr_str)
                    if addr is None:
                        raise ValueError("invalid address: " + str(addr_str))
                    if isinstance(data, list):
                        # Array of bytes
                        for i, byte_val in enumerate(data):
                            emulator.writeMemoryValue(addr.add(i), 1, byte_val & 0xff)
                    elif isinstance(data, str) and not data.startswith(("0x", "0X")):
                        # String data
                        for i, char in enumerate(data):
                            emulator.writeMemoryValue(addr.add(i), 1, ord(char))
                    else:
                        # Single value (int, or decimal/hex string)
                        v = data
                        if isinstance(v, str):
                            v = int(v, 16) if v.startswith(("0x", "0X")) else int(v)
                        emulator.writeMemoryValue(addr, 4, v)
                except Exception as e:
                    skipped_inputs.append({
                        "kind": "memory", "name": str(addr_str),
                        "value": data if isinstance(data, (int, str)) else str(data),
                        "reason": str(e)
                    })

            # Set up execution starting at function entry
            emulator.writeRegister(emulator.getPCRegister(), entry_point.getOffset())

            # Track execution
            execution_trace = []
            step_count = 0
            call_depth = 0
            stop_reason = "max_steps"

            # Execute until the function returns or max steps are hit. Calls are
            # followed into the callee: call_depth tracks how far we have wandered
            # from the original function, and only leaving its body at depth 0
            # counts as a return.
            while step_count < max_steps:
                current_addr = emulator.getExecutionAddress()

                if current_addr is None:
                    stop_reason = "no_execution_address"
                    break

                in_body = func.getBody().contains(current_addr)
                if not in_body and call_depth == 0:
                    # PC left the function without an outstanding call: returned
                    stop_reason = "returned"
                    break

                # Get current instruction (may be inside a callee)
                inst = program.getListing().getInstructionAt(current_addr)
                if inst is None:
                    stop_reason = "no_instruction_at_pc"
                    break

                flow = inst.getFlowType()
                is_call = flow.isCall()

                # Record trace
                trace_entry = {
                    "step": step_count,
                    "address": str(current_addr),
                    "instruction": inst.toString(),
                    "call_depth": call_depth
                }

                # Execute one instruction
                try:
                    success = emulator.step(monitor)
                    if not success:
                        trace_entry["error"] = "Execution failed"
                        execution_trace.append(trace_entry)
                        stop_reason = "execution_error"
                        break
                except Exception as e:
                    trace_entry["error"] = str(e)
                    execution_trace.append(trace_entry)
                    stop_reason = "execution_error"
                    break

                execution_trace.append(trace_entry)
                step_count += 1

                if is_call:
                    call_depth += 1
                elif flow.isTerminal():
                    if call_depth > 0:
                        # RET inside a callee: back to the caller's frame
                        call_depth -= 1
                    else:
                        stop_reason = "returned"
                        break

            # Collect final register states
            register_states = {}
            lang = emulator.getLanguage()

            # Get common registers based on architecture
            common_regs = []

            # Try to get architecture-specific registers
            if lang.getProcessor().toString().lower().startswith("x86"):
                # x86/x64 registers
                common_regs = ["RAX", "RBX", "RCX", "RDX", "RSI", "RDI", "RBP", "RSP",
                              "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15",
                              "RIP", "EAX", "EBX", "ECX", "EDX", "ESI", "EDI", "EBP", "ESP", "EIP"]
            elif lang.getProcessor().toString().lower().startswith("arm"):
                # ARM registers
                common_regs = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7",
                              "r8", "r9", "r10", "r11", "r12", "sp", "lr", "pc"]
            elif lang.getProcessor().toString().lower().startswith("mips"):
                # MIPS registers
                common_regs = ["v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1", "t2", "t3",
                              "t4", "t5", "t6", "t7", "s0", "s1", "s2", "s3", "s4", "s5",
                              "s6", "s7", "t8", "t9", "sp", "fp", "ra", "pc"]
            else:
                # Try to get all registers
                for reg in lang.getRegisters():
                    if not reg.isProcessorContext() and reg.getMinimumByteSize() >= 4:
                        common_regs.append(reg.getName())

            # Read register values
            for reg_name in common_regs:
                try:
                    reg = lang.getRegister(reg_name)
                    if reg is not None:
                        value = emulator.readRegister(reg)
                        register_states[reg_name] = "0x%x" % value
                except:
                    pass

            output_json({
                "status": "success",
                "function_name": func.getName(),
                "entry_point": str(entry_point),
                "steps_executed": step_count,
                "max_steps_reached": step_count >= max_steps,
                "stop_reason": stop_reason,
                "call_depth_at_stop": call_depth,
                "skipped_inputs": skipped_inputs,
                "register_states": register_states,
                "execution_trace": execution_trace[:100],  # Limit trace to first 100 steps
                "trace_truncated": len(execution_trace) > 100
            })

        finally:
            emulator.dispose()

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

# Run the script
run()
