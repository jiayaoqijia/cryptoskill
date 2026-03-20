import { defineProject } from "vitest/config";

export default defineProject({
  test: {
    name: "shared",
    environment: "node",
  },
});
