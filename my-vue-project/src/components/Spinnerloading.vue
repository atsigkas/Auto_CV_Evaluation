<template>
    <div>
      <div v-if="spinner.isVisible" class="spinner-wrapper">
        <div class="spinner">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
        <span class="spinner-message">{{ spinner.message }}</span>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex';

  export default {
    name: "SpinnerLoading",
    computed: {
    ...mapState(['spinner']),
    }
  };
  </script>
  
  <style scoped>
  .spinner-wrapper {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 999;
  }
  
  .spinner-wrapper:before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
  }
  .spinner-message {
    margin-top: 10px;
    color: #fff;
    z-index: 10;
  }
  .spinner {
    display: inline-block;
    position: relative;
    width: 80px;
    height: 80px;

  }
  .spinner div {
    box-sizing: border-box;
    display: block;
    position: absolute;
    width: 64px;
    height: 64px;
    margin: 8px;
    border: 8px solid rgb(49, 247, 253);
    border-radius: 50%;
    animation: spinner 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    border-color: rgb(49, 247, 253) transparent transparent transparent;
  }
  .spinner div:nth-child(1) {
    animation-delay: -0.45s;
  }
  .spinner div:nth-child(2) {
    animation-delay: -0.3s;
  }
  .spinner div:nth-child(3) {
    animation-delay: -0.15s;
  }
  @keyframes spinner {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  </style>
  