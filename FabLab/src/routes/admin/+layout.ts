import { browser } from '$app/environment';
import { base } from '$app/paths';
import { get } from 'svelte/store';
import { isLoggedIn, currentUser } from '../../lib/index.ts';
import { GET } from '../../ts/server.ts';
import type { User } from '../../modelse/User.ts';

export const load = async () => {
    if (browser) {
        if (get(isLoggedIn)) return;
        try {
            const user = await GET<User>('/user/me', false);
            currentUser.set(user);
            isLoggedIn.set(true);
        } catch {
            window.location.href = `${base}/login`;
        }
    }
};