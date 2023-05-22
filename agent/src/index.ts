import { hook } from "./hooking"

rpc.exports = {
	hook: (modules: string[], customModules: string[]): boolean => hook(modules, customModules),
};