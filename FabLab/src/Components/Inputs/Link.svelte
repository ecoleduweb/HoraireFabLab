<script lang="ts">
    export let text: string
    export let href: string = text.toLowerCase()
</script>

<a {href}>{text}</a>

<style scoped>
    a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease; /* Add a smooth transition */
    }

    a:hover {
        background-color: #b3b3b3;
    }
</style>
