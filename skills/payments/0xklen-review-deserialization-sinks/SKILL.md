---
name: review-deserialization-sinks
description: Use when untrusted bytes reach a native deserializer such as pickle, Java ObjectInputStream, PHP unserialize, or .NET BinaryFormatter. Finds the sinks, rates exploitability, and replaces them with data-only formats.
---

# Review deserialization sinks

Deserializers that can instantiate arbitrary classes turn attacker bytes into attacker code, via
gadget chains that need no bug in your own code. The durable fix is to stop feeding untrusted input
to a class-constructing format.

## Procedure

1. Enumerate dangerous sinks per language:

       rg -n "pickle\.loads?|cPickle|dill\.loads|yaml\.load\(|marshal\.loads" .          # Python
       rg -n "ObjectInputStream|readObject\(|XStream|SnakeYAML|readValue\(" .            # Java
       rg -n "unserialize\(|session_decode|igbinary_unserialize" .                        # PHP
       rg -n "BinaryFormatter|NetDataContractSerializer|LosFormatter|TypeNameHandling" . # .NET
       rg -n "node-serialize|serialize-javascript|unserialize\(" .                        # Node

2. Classify each hit by reachability: is the byte stream from a request body, a cookie, a cache, a
   queue message, or a file written by an untrusted party? A sink with no untrusted source is not
   exploitable — say so explicitly rather than flagging it.

3. Python YAML: `yaml.load(x)` without a `Loader` is remote code execution;
   `yaml.safe_load(x)` is the fix when the document is pure data.

4. Java: `ObjectInputStream.readObject` on untrusted bytes is exploitable via gadget chains in the
   classpath (commons-collections, Spring). Prefer JSON with an explicit target class; if native
   serialization is unavoidable, use a `ObjectInputFilter` allowlist of classes.

5. PHP: `unserialize()` on cookies or request data, plus `phar://` wrappers that trigger object
   magic methods on file functions, are the two routes. Replace with `json_decode`.

6. .NET: `BinaryFormatter` is deprecated as inherently unsafe; `TypeNameHandling.All` in
   Json.NET is the JSON equivalent of the bug. Set `TypeNameHandling.None`.

7. Prove the exposure with a benign payload that would run only if deserialization executes:

       # Python — this prints PWNED only if yaml.load is unsafe
       python3 -c "import yaml; print(yaml.load('!!python/object/apply:os.system [\"echo PWNED\"]'))"

8. If a signed blob must be deserialized, verify a MAC over the bytes *before* deserialising, using
   a constant-time comparison; the signature gates the parser.

## Pitfalls

- `yaml.safe_load` still allows `!!python/name` aliases in some bindings; test rather than assume.
- A gadget chain needs one class on the classpath — a framework dependency you forgot is enough.
- JSON is not automatically safe: polymorphic deserialization (`TypeNameHandling`, Java
  `@JsonTypeInfo`) reintroduces class construction.
- Signing without verifying, or verifying after parsing, gives no protection.
- Cached serialized objects across a deploy can be loaded by the new class version — a deserialise
  of a stale blob is still untrusted.
- `phar://` deserializes on mere filesystem calls (`file_exists`), not just on `unserialize`.

## Verification

    python3 -c "import yaml; print(yaml.load('!!python/object/apply:os.system [\"echo PWNED\"]'))" 2>&1 \
      | rg -q PWNED && echo "VULNERABLE" || echo "safe"

Pass: after the fix the probe prints `safe` (safe_load rejects the tag), and the Java/.NET sink
list shows zero untrusted-reachable hits. Report each sink, its input source, and the replacement
format adopted.
