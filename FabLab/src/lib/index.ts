import { writable } from "svelte/store";
import type { User } from "../modeles/User.ts";

export const isLoggedIn = writable(false);
export const currentUser = writable<User | undefined>();
