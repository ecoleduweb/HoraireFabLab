<script lang="ts">
    import { goto } from "$app/navigation"
    import { isLoggedIn, currentUser } from "../../lib/index.ts"
    import { POST } from "../../ts/server.ts"
    import { base } from "$app/paths"

    const handleLogout = async () => {
        try {
            await POST("/logout", {}, false)
        } catch (error) {
            console.error("Error during logout:", error)
        }
        isLoggedIn.set(false)
        currentUser.set(undefined)
        goto(`${base}/login`)
    }
</script>

<header>
    <div class="logo-img">
        <a href="{base}/admin" class="image">
            <img src="{base}/logo.png" alt="Logo" />
        </a>
    </div>

    <div class="actions">
        {#if $isLoggedIn}
            <span class="username">{$currentUser?.username}</span>
            <button class="logout-button" onclick={handleLogout}>
                <img src="{base}/logout.svg" alt="Déconnexion" class="icone" />
                <span>Déconnexion</span>
            </button>
        {/if}
    </div>
</header>

<style>
    header {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        height: 60px;
        background-color: #1e2634;
        border-bottom: 1px solid #00ad9a;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        padding: 0 2rem;
        box-sizing: border-box;
    }

    .logo-img {
        display: flex;
        align-items: center;
    }

    .image img {
        height: 36px;
        width: auto;
    }

    .actions {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .username {
        color: #aaa;
        font-family: var(--fb);
        font-size: 14px;
    }

    .logout-button {
        display: flex;
        align-items: center;
        gap: 6px;
        background: transparent;
        border: 1px solid #555;
        border-radius: 6px;
        color: white;
        font-family: var(--fb);
        font-size: 14px;
        padding: 6px 12px;
        cursor: pointer;
        transition: border-color 0.2s, background-color 0.2s;
    }

    .logout-button:hover {
        border-color: #00ad9a;
        background-color: rgba(0, 173, 154, 0.08);
    }

    .icone {
        width: 18px;
        height: 18px;
        filter: invert(1);
    }
</style>