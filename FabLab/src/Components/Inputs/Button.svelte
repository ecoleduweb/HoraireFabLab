<script lang="ts">
    export let text: string
    export let submit: boolean = false
    export let onClick: (() => void) = () => {}
    export let cssId: string = ""
</script>

{#if submit}
    <input id={cssId} type="submit" class="submit" value={text} />
{:else}
    <button id={cssId} class="button" on:click={onClick}>{text}</button>
{/if}

<style scoped>
    /* Dropdown Button */
    .button {
        color: white;
        padding: 10px 15px;
        font-size: 16px;
        border: none;
        border-radius: 14px;
        cursor: pointer;
        background: linear-gradient(
                90deg,
                var(--c1, #992050),
                var(--c2, #ab223a) 50%,
                var(--c3, #329b8d) 0%,
                var(--c4, #37ad9a) 80%
            )
            var(--x, 0) / 200%;
    }

    .submit {
        color: white;
        padding: 10px 15px;
        font-size: 16px;
        border: none;
        border-radius: 14px;
        cursor: pointer;
        transition: 0.5s;
        background: linear-gradient(
                90deg,
                var(--c1, #329b8d),
                var(--c2, #37ad9a) 45%,
                var(--c3, #992050) 60%,
                var(--c4, #ab223a) 85%
            )
            var(--x, 0) / 200%;
    }

    .button:hover,
    .submit:hover {
        --x: 100%;
    }
</style>
