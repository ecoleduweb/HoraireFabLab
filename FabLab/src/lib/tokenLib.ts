import { jwtDecode } from "jwt-decode";
import type Token from "../Models/Token.ts";
import { currentUser, isLoggedIn } from "../lib/index.ts";
import { goto } from "$app/navigation";

const LocalStorageKey = "token"

export const decodeToken = (): Token | null => {
  const token = localStorage.getItem(LocalStorageKey)
  return token ? jwtDecode<Token>(token) : null
}

export const isTokenExpired = () => {
  const decoded = decodeToken()
  const currentTime = Math.floor(Date.now() / 1000);
  return decoded ? decoded.exp < currentTime : true;
}

export const disconnectUser = () => {
  localStorage.token = undefined
  currentUser.set(undefined)
  isLoggedIn.set(false)
}

export const logIn = (token: any) => {
  if (token != "") {
    localStorage.setItem(LocalStorageKey, token)

    const decodedUser = jwtDecode(token) as any
    setInfoFromDecoded(decodedUser)
    goto("/dashboard")
  }
}

export const setInfoFromDecoded = (decoded: any) => {
  currentUser.set(decoded)
  isLoggedIn.set(true)
}