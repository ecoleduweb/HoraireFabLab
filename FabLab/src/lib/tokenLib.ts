import { currentUser, isLoggedIn } from "./index.ts";
import { goto } from "$app/navigation";
import type { User } from "../Models/User.ts";


export const logIn = async (user: User) => {
  currentUser.set(user)
  isLoggedIn.set(true)
  await goto("/test")
}

export const setInfoFromDecoded = (decoded: any) => {
  currentUser.set(decoded)
  isLoggedIn.set(true)
}