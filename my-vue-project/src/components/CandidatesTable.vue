<template>
    <div class="tab-content" id="candidates-tab-content">
        <form @submit.prevent="candidateForm">
            <table class="candidates-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Publication</th>
                    <th>Articles</th>
                    <th>Conference</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <template v-for="(candidate,index) in candidates" :key="index">
                    <tr>
                        <td>{{candidate.author }}</td>
                        <td>{{candidate.email }}</td>
                        <td>PASOK</td>
                        <td>PASOK</td>
                        <td>PASOK</td>
                        <td>
                            <div class="actions-wrapper">
                                <button v-if="candidate.publication" type="button" class="candidate-icon candidate-show" @click="publicationEdit()">
                                    <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25">
                                    </path>
                                    </svg> 
                                </button>
                                <button v-if="candidate.researchgate_url =='' && candidate.googlescholar_url =='' " class="candidate-icon candidate-edit" @click="candidateEditUrl({ id: 'candidate-id-1' })">
                                    <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125">
                                    </path>
                                    </svg> 
                                </button>
                            </div>
                        </td>
                    </tr>
                    <tr class="candidate-url-row" id="candidate-id-1">
                        <td colspan="1" style="border-right:0">
                            URL :
                        </td>
                        <td colspan="3">
                            <input type="text" name="'candidate-id-1" class="candidate-url" value="">
                        </td>
                        <td colspan="1">
                            <button type="submit" class="submit-button submit-button--small save-url-btn"
                            @click="saveUrl({ id: 'candidate-id-1' })">Save</button>
                        </td>
                    </tr>
                    
                </template>
            </tbody>
            </table>
            <button type="submit" class="submit-button submit-button--small candidate-submit"
            @click="submitCandidates">Submit</button>
        </form>
        <div v-if="showPublications">
      <div class="dialog-box">
        <div class="dialog-wrapper">
          <form @submit.prevent="submitPublications">
            <h2 class="dialog-title">Dialog Title</h2>
            <div class="list-wrapper">

              <ul class="list list--found">
                <li class="list-head">
                  <h3>Found</h3>
                </li>
                <li>title1</li>
                <li>title2</li>
                <li>title3</li>
              </ul>
              <div class="list-separator"></div>
              <ul class="list list--notfound">
                <li class="list-head">
                  <h3>Not Found</h3>
                </li>
                <li><span class="list-title">title1</span>
                  <div class="cbox-wrapper">
                    <input type="checkbox">
                    <span class="checkmark"></span>
                  </div>
                </li>
                <li><span class="list-title">title2</span>
                  <div class="cbox-wrapper">
                    <input type="checkbox">
                    <span class="checkmark"></span>
                  </div>
                </li>
                <li><span class="list-title">title3</span>
                  <div class="cbox-wrapper">
                    <input type="checkbox" checked>
                    <span class="checkmark"></span>
                  </div>
                </li>
              </ul>
            </div>
            <div class="dialog-actions">
              <button class="submit-button submit-button--small" @click="closeDialog">Cancel</button>
              <button class="submit-button submit-button--small" type="submit">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
export default { 
    name:'CandidatesTable',
    props: {
        candidates: {
            type: Array,
            required: true,
        }
    },
    data(){
        return{
            showPublications: false,
        };
    },
    methods: {
        candidateForm(event) {
        event.preventDefault()
        //TODO
        },
        publicationEdit() {
        this.showPublications = true
        },
        candidateEditUrl({ id }) {
        const inputRow = document.getElementById(id)
        inputRow.classList.toggle('active')
        },
        saveUrl({ id }) {
        const inputRow = document.getElementById(id)
        inputRow.classList.remove('active')
        
        },
        submitCandidates() {
        // Handle submit candidates
        //TODO
        },
        closeDialog() {
        this.showPublications = false
        }
    },mounted() {
        this.showPublications - false;
    },
}
</script>

<style src="./CandidatesTable.css"></style>
