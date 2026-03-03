<script lang="ts">
	import { goto } from "$app/navigation";

    const handleBtnClick = async () => {
	    await goto("/login");
	};
    
</script>

<section>
	<h1>It works!</h1>
	<button onclick={handleBtnClick}>Go back to login</button>
</section>