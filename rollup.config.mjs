import resolve from "@rollup/plugin-node-resolve";

export default {
  input: "src/scripts/app.js",
  output: {
    file: "public/scripts/app.js",
    format: "esm",
  },
  plugins: [resolve()],
};
