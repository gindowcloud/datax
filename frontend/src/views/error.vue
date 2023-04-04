<template>
  <div class="error">
    <div class="code">404</div>
    <div class="text">页面未找到</div>
    <div class="route">{{ $route.fullPath }}</div>
  </div>
</template>

<style scoped>
.error { height: 100vh; text-align: center; font-weight: 200; color: #444; }
.error .code { font-size: 50px; padding-top: calc(50vh - 100px); }
.error .text { font-size: 18px; }
.error .route { position: fixed; width: 100%; bottom: 15px; color: #ddd; }
</style>
