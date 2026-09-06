---
name: controller-integration
description: >
  Wire a new or existing controller — whether imported from a
  `@metamask/*-controller` npm package or defined locally in the repo — into
  the MetaMask Mobile Engine or the MetaMask Extension background. Use this
  skill when: adding a controller to Engine or to the extension's
  messenger-client init, creating a controller init function or messenger,
  delegating actions/events between controllers, adding a controller to
  EngineState/Engine.context or to MESSENGER_FACTORIES and the
  MessengerClient union, or debugging a controller whose state never reaches
  Redux/the UI or resets on restart.
base: true
---
