import adapter from '@sveltejs/adapter-node';
import { loadEnv } from 'vite';

const env = loadEnv(process.env.NODE_ENV || 'development', process.cwd(), '');

const basePath = env.BASE_PATH || '';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    kit: {
        adapter: adapter(),
        paths: {
            base: basePath
        }
    }
};

export default config;

