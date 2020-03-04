<template>
  <div class="container">
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeName: 'first',
      showTeam: false,
    }
  },
  mounted() {
    if (document.body.clientWidth > 1200 && document.body.clientWidth < 1330) {
      this.showTeam = true
    }
  },
  methods: {
  },
}
</script>

<style scoped lang="scss">
.container {
  padding: 20px;
}

@media screen and (max-width: 1200px) {
  .container {
    display: none;
  }
  .container {
    width: 100%;
  }
  .container {
    width: 32%;
    &:last-child {
      display: none;
    }
  }
  .container {
    display: none;
  }
}

@media screen and (max-width: 1200px) {
  .container {
    width: 100%;
  }
}
</style>
