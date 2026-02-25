import { writable} from "svelte/store";
type Session={
    isLoggedIn: boolean;
}

export const session = writable<Session>({
    isLoggedIn: false,
});