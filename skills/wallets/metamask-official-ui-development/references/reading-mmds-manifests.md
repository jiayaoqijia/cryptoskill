# Reading the MMDS components manifests

MMDS publishes a Storybook components manifest for each platform:

| Platform | Manifest |
| --- | --- |
| React (Extension) | <https://metamask.github.io/metamask-design-system/manifests/components.json> |
| React Native (Mobile) | <https://metamask.github.io/metamask-design-system/react-native/manifests/components.json> |

The React Storybook also publishes intro docs at
<https://metamask.github.io/metamask-design-system/manifests/docs.json>.
React Native does not publish a `docs.json`.

This file explains the format. It deliberately lists no components, versions,
or props: read those from the manifest and the installed package.

## What the manifest is

- It is generated from the Storybook build of MMDS `main`. It can be ahead of
  the version a consumer repo installs, so a component or prop in the manifest
  may not exist in `node_modules` yet. The installed types decide.
- It is large (a few MB). Fetch it once and search it, for example with
  `curl -s <url> | jq` or a script, rather than reading it whole.
- It is a discovery and deprecation index for a component's own API. Prop
  data is extracted with react-docgen-typescript (`meta.docgen`).

## Shape

```text
{
  "v": <format version>,
  "components": {
    "<story id>": {
      "id":          "<story id>",
      "name":        "<ComponentName>",
      "path":        "<story file in the MMDS repo>",
      "import":      "<import line(s) used by the stories>",
      "jsDocTags":   { "deprecated": ["<reason and replacement>"] },
      "reactDocgenTypescript": {
        "description": "...",
        "props": {
          "<prop>": {
            "required": ...,
            "description": "...",
            "declarations": [ { "fileName": "...", "name": "..." } ],
            "type": {
              "name": "<type name>",
              "raw": "<source text, enums>",
              "value": [ { "value": "<enum member>" } ]
            }
          }
        }
      },
      "stories": [ { "id": "...", "name": "...", "snippet": "<example JSX>" } ]
    }
  },
  "meta": { "docgen": "react-docgen-typescript" }
}
```

Prop data lives under `reactDocgenTypescript.props`. Read `type.name`. Enums
also set `type.raw` and `type.value`, and `type.value` lists the members.
`declarations` records where the prop is declared. Entries are keyed by
Storybook story id, not by component name.

Treat an entry as a component only when its `path` is a story under the
platform package's `src/components/` (including `temp-components/`) and the
component name appears in the installed export index.

## Which props appear

- Props declared on the component, including props defined in the shared types
  package, appear in the manifest.
- `className`, `style`, `children`, and `testID` are always kept. A component
  that does not accept one of them does not list it.
- Other host or native element props (DOM attributes, `ViewProps`) are
  filtered out.
- The manifest is reliable for a component's own API. Check the component's
  installed types for anything it inherits from the host element.

Not every story is in the components manifest. A missing entry is not proof
that no story or pattern exists. Follow the pattern lookup order in the
`ui-development` skill.

## Common queries

- **Is there a component for X?** Look up the component by name in the
  manifest: search `name` and `reactDocgenTypescript.description`, then
  confirm the name is exported by the installed package index.
- **Is there already a pattern?** Look in this manifest and the docs manifest,
  then follow the pattern lookup order in the `ui-development` skill. Use the
  first place that has it.
- **Is it deprecated?** A non-empty `jsDocTags.deprecated` means deprecated,
  and the message usually names the replacement. How to confirm it and what
  to do: the Deprecated APIs section of the `ui-development` skill.
- **Which props does it take?** `reactDocgenTypescript.props` gives the name,
  `required`, description, `declarations`, and `type` for `main`. Read
  `type.name`. For an enum, `type.value` lists the members. Confirm each prop
  in the installed types before using it, including host props the manifest
  filters out.
- **How is it used?** `stories[].snippet` shows example JSX.

## Caveats

- `import` lines come from MMDS story files. They may import enums from
  `@metamask/design-system-shared` or use relative paths. In product code,
  import components and enums from the platform package
  (`@metamask/design-system-react` or `@metamask/design-system-react-native`).
- Do not copy manifest content into a skill. It changes with every MMDS merge.
