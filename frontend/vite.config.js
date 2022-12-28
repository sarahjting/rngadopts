import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from 'path'
import { readdirSync } from 'fs'

// taken from https://stackoverflow.com/questions/69424422/use-compileroptions-baseurl-with-vite-js-project
// i'm running this project with vite, but creativetim's layout template was built using CRA
// vite does not natively support absolute path imports; we need to fiddle with the aliasing a little to support this
const absolutePathAliases = {};

// Root resources folder
const srcPath = path.resolve('./src');

// Adjust the regex here to include .vue, .js, .jsx, etc.. files from the resources/ folder
const srcRootContent = readdirSync(srcPath, { withFileTypes: true }).map((dirent) => dirent.name.replace(/(\.js){1}(x?)/, ''));

srcRootContent.forEach((directory) => {
  absolutePathAliases[directory] = path.join(srcPath, directory);
});

// https://vitejs.dev/config/
export default defineConfig({
  build: { 
    manifest: true,
  },
  base: process.env.mode === "production" ? "/static/" : "/",
  plugins: [react()],
  resolve: {
    alias: {
      ...absolutePathAliases
    }
  },
});
