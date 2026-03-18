import adapter from '@sveltejs/adapter-node';

const config = {
    kit: {
        adapter: adapter(),
        paths: {
            base: '/fablab-frontend'
        }
    }
};

export default config;
