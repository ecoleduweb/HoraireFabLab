<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import type { Login } from "../../Models/Login.ts"
    import { POST } from "../../ts/server.ts"
    import * as yup from "yup"
    import { extractErrors } from "../../ts/utils.ts"
    import { logIn } from "../../lib/tokenLib.ts"
	import type { User } from "../../Models/User.ts";

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
                const response = await POST<Login, User>("/login", form, false)
                logIn(response.data)
            } catch (err) {
                console.error("Login error:", err);
                errors = {
                    username: "",
                    password: "Nom d'utilisateur ou mot de passe invalide",
                    email: undefined,
                    phone: undefined
                }
            }
            //Petite modification de la gestion de l'erreur
            } catch (err) {
            if (err instanceof yup.ValidationError) {
                errors = extractErrors<Login>(err)
            }
        }  
    } 
</script>

<section>
    <div class="login">
        <h1>Authentification</h1>

        <form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="login-form">
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
:global {
    section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #f5f5f5;
    }

    h1 {
    width: 100%;
    text-align: center;
    color: #1a1a1a;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 10px;
    }

    .login {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 1px solid #ccc;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        padding: 20px;
        width: 22%;
        background-color: #fff;
    }

    .input-login {
        width: 70%;
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 4px;
        color: #1a1a1a;
        background-color: #ffffff;          /* ← ajouté */
        -webkit-text-fill-color: #1a1a1a;  /* ← pour autofill Chrome */
    }

    .input-login:-webkit-autofill {
        -webkit-box-shadow: 0 0 0px 1000px #ffffff inset;  /* ← fond autofill */
        -webkit-text-fill-color: #1a1a1a;
    }

    .errors-input {
        color: #cc0000;        /* ← ajouté, texte erreur en rouge */
        font-size: 0.8rem;
        margin: 2px 0 6px 0;
        min-height: 1rem;      /* ← évite le layout shift quand vide */
    }

    .login-form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        padding: 20px;
    }

    .login-form label {
        color: black;
    }

    label {
        margin-bottom: 8px;
    }

    .submit {
        margin: 10px;
    }

    @media screen and (max-width: 900px) and (min-width: 300px) {
        .login {
            width: 50%;
        }
    }
}
</style>
