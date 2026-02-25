<script lang="ts">
    import { goto } from "$app/navigation"
    import { onMount } from "svelte"
    import { isLoggedIn, currentUser } from "../../lib/index.ts"
    import { GET, POST } from "../../ts/server.ts"
    import { Hamburger } from "svelte-hamburgers"
    import type { User } from "../../Models/User.ts"

    let open = $state<boolean>(false)

    const checkSession = async () => {
        try {
            const me = await GET<{ user: User }>("/user/me", false)
            currentUser.set(me as any)
            isLoggedIn.set(true)
        } catch {
            currentUser.set(undefined)
            isLoggedIn.set(false)
        }
    }

    onMount(async () => {
        await checkSession()
    })

    const handleDashboard = () => {
        open = false
        goto("/dashboard")
    }
    const handleUtilisateur = () => {
        open = false
        goto("/users")
    }
    const handleProfile = () => {
        open = false
        goto("/profile")
    }
    const handleLogin = () => {
        open = false
        goto("/login")
    }
    const handleRegister = () => {
        open = false
        goto("/register")
    }

    const handleLogout = async () => {
        open = false
        try {
            await POST("/user/logout", {}, false)
        } catch (error) {
            console.error("Error during logout:", error)
        }
        isLoggedIn.set(false)
        currentUser.set(undefined)
        goto("/login")
    }
</script>

<header>
    <div class="logo-img">
        <a href="/" class="image"><img src="logo.png" alt="Logo" /></a>
    </div>
    <!--MENU MOBILE --------------------------- -->
    <div class={$isLoggedIn ? "burger" : "burger-disconnected"}>
        <Hamburger bind:open --color="white" />
        {#if open}
            <div class="menu-dropdown">
                {#if $currentUser}
                    <div class="option">
                        <button class="button" onclick={handleUtilisateur}>
                            <p class="textSearch">Utilisateurs</p>
                        </button>
                        <button class="button" onclick={handleDashboard}>
                            <p class="textSearch">Tableau de bord</p>
                            <img
                                class="iconeLogout"
                                src="searchBar.svg"
                                alt="Search icon"
                            />
                        </button>
                        <button class="button" onclick={handleProfile}>
                            <p class="textSearch">
                                Connecté en tant que : {$currentUser?.username}
                            </p>
                        </button>
                        <button class="button" onclick={handleLogout}>
                            <p class="textSearch">Déconnexion</p>
                            <img
                                class="iconeLogout"
                                src="logout.svg"
                                alt="Logout icon"
                            />
                        </button>
                    </div>
                {/if}
                {#if !$isLoggedIn}
                    <div class="option">
                        <button class="button" onclick={handleLogin}>
                            <p class="textSearch">Connexion entreprise</p>
                            <img
                                class="iconeLogout"
                                src="business.svg"
                                alt="Business icon"
                            />
                        </button>
                        <button class="button" onclick={handleRegister}>
                            <p class="textSearch">Créer un compte entreprise</p>
                            <img
                                class="iconeLogout"
                                src="add.svg"
                                alt="Add icon"
                            />
                        </button>
                    </div>
                {/if}
            </div>
        {/if}
    </div>
    <!--MENU MOBILE FIN --------------------------- -->

    <div class="ul-group">
        <ul class="ul-menu">
            {#if $currentUser && $isLoggedIn}
                <style scoped>
                    .logo-img {
                        width: 40% !important;
                    }
                </style>

                <div class="option">
                    <button
                        class="button logout-button"
                        onclick={handleUtilisateur}
                    >
                        <p class="textLogout">Utilisateurs</p>
                    </button>
                </div>

                <div class="option">
                    <button
                        class="button logout-button"
                        onclick={handleDashboard}
                    >
                        <p class="textLogout">Tableau de bord</p>
                        <img
                            class="iconeSearch"
                            src="searchBar.svg"
                            alt="Search icon"
                        />
                    </button>
                </div>
                <div class={"dropdown-content-profile-admin"}>
                    <a href="/profile">Modifier mon profil </a>
                    <a href="/" onclick={handleLogout}>Déconnexion</a>
                </div>
            {/if}
        </ul>
    </div>
</header>

<style scoped>
    @import "../../styles/header.css";
</style>