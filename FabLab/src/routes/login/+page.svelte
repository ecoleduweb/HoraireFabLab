<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import type { Login } from "../../Models/Login.ts"
    import { POST } from "../../ts/server.ts"
    import * as yup from "yup"
    import { extractErrors } from "../../ts/utils.ts"
    import { isLoggedIn } from "../../lib/index.ts"
    import { disconnectUser, isTokenExpired, logIn } from "../../lib/tokenLib.ts"

    const schema = yup.object().shape({
        username: yup
            .string()
            .required("Entrer un nom d'utilisateur"),
        password: yup.string().required("Le mot de passe est requis"),
        email: yup.string().notRequired(),
        phone: yup.string().notRequired()
    })

    let errors = $state<Login>({
        username: "",
        password: "",
        email: undefined,
        phone: undefined
    })

    let form = $state<Login>({
        username: "",
        password: "",
        email: undefined,
        phone: undefined
    })

    const handleSubmit = async () => {
        try {
            await schema.validate(form, { abortEarly: false })

            errors = {
                username: "",
                password: "",
                email: undefined,
                phone: undefined
            }

            try {
                const response = await POST<Login, any>("/login", form, false)
                logIn(response.data.token)
            } catch {
                errors = {
                    username: "",
                    password: "Courriel ou mot de passe invalide",
                    email: undefined,
                    phone: undefined
                }
            }
        } catch (err) {
            errors = extractErrors(err)
        }
    }

    $effect(() => {
        if ($isLoggedIn && isTokenExpired()) {
            disconnectUser()
        }
    })
</script>

<section>
    <div class="login">
        <h1>Authentification</h1>

        <form on:submit|preventDefault={handleSubmit} class="login-form">
            <label for="username">Nom d'utilisateur</label>
            <input
                type="text"
                class="input-login"
                id="username"
                name="username"
                bind:value={form.username}
            />
            <p class="errors-input">
                {#if errors.username}{errors.username}{/if}
            </p>

            <!--If email and/or phone fields are needed, take out the comment tags and they will be available and working-->
            <!--
            <label for="email">Courriel</label>
            <input
                type="text"
                class="input-login"
                id="email"
                name="email"
                bind:value={form.email}
            />
            <p class="errors-input">
                {#if errors.email}{errors.email}{/if}
            </p>
            <label for="phone">Téléphone</label>
            <input
                type="text"
                class="input-login"
                id="phone"
                name="phone"
                bind:value={form.phone}
            />
            <p class="errors-input">
                {#if errors.phone}{errors.phone}{/if}
            </p>
            -->

            <label for="password">Mot de passe</label>
            <input
                type="password"
                class="input-login"
                id="password"
                name="password"
                bind:value={form.password}
            />
            <p class="errors-input">
                {#if errors.password}{errors.password}{/if}
            </p>

            <Button text="Se connecter" submit={true} />
        </form>
    </div>
</section>

<style scoped>
    @import "../../styles/login.css";
</style>
