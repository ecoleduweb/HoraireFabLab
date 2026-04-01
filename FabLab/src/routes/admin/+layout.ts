import { browser } from '$app/environment';
import { base } from '$app/paths';
import { get } from 'svelte/store';
import { isLoggedIn } from '../../lib/index.ts';
 
export const load = () => {
    if (browser && !get(isLoggedIn)) {
        window.location.href = `${base}/login`;
    }
};