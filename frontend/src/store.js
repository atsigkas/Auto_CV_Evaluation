import { createStore } from 'vuex';

export default createStore({
  state: {
    functionName: '',
    spinner: {
      isVisible: false,
      message: ''
    },
    dialog: {
      isVisible: false,
      message: ''
    }
  },
  mutations: {
    setFunctionName(state, functionName) {
      state.functionName = functionName;
      state.dialog.message = '';
    },
    showSpinner(state, message) {
      state.spinner.isVisible = true;
      state.spinner.message = message;
    },
    hideSpinner(state) {
      state.spinner.isVisible = false;
      state.spinner.message = '';
    },
    showDialog(state, message) {
      state.dialog.isVisible = true;
      state.dialog.message = message;
    },
    hideDialog(state) {
      state.dialog.isVisible = false;
    }
  },
  actions: {
    setFunctionName({ commit }, functionName) {
      commit('setFunctionName', functionName);
    },
    showSpinner({ commit }, message) {
      commit('showSpinner', message);
    },
    hideSpinner({ commit }) {
      commit('hideSpinner');
    },
    showDialog({ commit }, message) {
      commit('showDialog', message);
    },
    hideDialog({ commit }) {
      commit('hideDialog');
    }
  }
});