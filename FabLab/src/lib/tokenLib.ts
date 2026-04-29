import { currentUser, isLoggedIn } from "./index.ts";
import { goto } from "$app/navigation";
import { base } from "$app/paths";
import type { User } from "../modelse/User.ts";

export const logIn = async (user: User) => {
  currentUser.set(user);
  isLoggedIn.set(true);
  await goto(`${base}/admin`);
}

export const logOut = async () => {
    currentUser.set(undefined);
    isLoggedIn.set(false);
    await goto(`${base}/login`);
}

export const setInfoFromDecoded = (decoded: any) => {
  currentUser.set(decoded)
  isLoggedIn.set(true)
}