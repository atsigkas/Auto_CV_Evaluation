<template>
  <div v-if="dialog.isVisible" class="dialog">
    <div class="dialog-box dialog-box--small">
      <div class="dialog-wrapper">
          <div class="dialog-textarea">{{ dialog.message }}</div>
          <div class="dialog-actions">
            <button class="dialog-button" @click="closeDialog">OK</button>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState(['dialog']),
  },
  methods: {
    closeDialog() {
      if (this.dialog.message == 'Pdf are uploaded.') {
        this.$store.dispatch('setFunctionName', "toggleSidebar");
      }
      this.$store.dispatch('hideDialog');
    }
  }
};
</script>

<style>

.dialog-button {
  position: relative;
  background-color: rgba(var(--gold), 0.8);
  color: white;
  padding: 10px 10px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  white-space: nowrap;
  border-radius: 20px;
  font-weight: bold;
  height: 30px;
  width: 50px;
  transition: background-color 0.3s ease-out;
}

.dialog-textarea{
  text-align: center;
  margin-bottom: 20px;
}

</style>
