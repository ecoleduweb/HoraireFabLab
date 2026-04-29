import { writable } from "svelte/store";
import type { User } from "../modelse/User.ts";

export const isLoggedIn = writable(false);
export const currentUser = writable<User | undefined>();
