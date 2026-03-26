
<script lang="ts">
	import { goto } from "$app/navigation";
	import { resolve } from "$app/paths";

	const handleBtnClick = async () => {
		await goto(resolve("/login"));
	};
    
</script>

<section style="background-color: white; height: 100vh;">
	<h1>It works!</h1>
	<button onclick={handleBtnClick}>Go back to login</button>
</section>