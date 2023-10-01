<template>
  <div class="tab-content" id="candidates-tab-content">
    <form v-if="this.localCandidates.length > 0" @submit.prevent="candidateForm">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Publications</th>
            <th>Articles</th>
            <th>Conferences</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="({ candidate, totalArticles, totalConference }, index) in localCandidates" :key="index">
            <tr>
              <td>{{ candidate.author }}</td>
              <td>{{ candidate.email }}</td>
              <td>{{ candidate.publication.length }}</td>
              <td>{{ totalArticles }}</td>
              <td>{{ totalConference }}</td>
              <td>
                <div class="actions-wrapper">
                  <button v-if="candidate.publication && candidate.researchgate_url !='' || candidate.googlescholar_url!=''" type="button" class="candidate-icon candidate-show"
                    @click="publicationEdit({ index })">
                    <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25">
                      </path>
                    </svg>
                  </button>
                  <button v-if="candidate.researchgate_url == '' && candidate.googlescholar_url == ''"
                    class="candidate-icon candidate-edit" @click="candidateEditUrl({ id: 'candidate-id-' + index })">
                    <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125">
                      </path>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
            <tr class="candidate-url-row" :id="`candidate-id-${index}`">
              <td colspan="1" style="border-right:0">
                URL :
              </td>
              <td colspan="4">
                <input type="text" :name="`candidate-id-${index}`" class="candidate-url" value="">
              </td>
              <td colspan="1">
                <button type="submit" class="submit-button submit-button--small save-url-btn"
                  @click="saveUrl({ id: 'candidate-id-' + index })">Save</button>
              </td>
            </tr>

          </template>
        </tbody>
      </table>
      <button type="submit" class="submit-button submit-button--small candidate-submit"
        @click="submitCandidates">Submit</button>
    </form>
    <div v-if="showPublications" class="dialog">
      <div class="dialog-box">
        <div class="dialog-wrapper">
          <form @submit.prevent="submitPublications">
            <h2 class="dialog-title">Publications of the Candidate :
              <span class="dialog-name">{{ this.localCandidates[this.localIndex].candidate.author }}</span>
            </h2>
            <div class="list-wrapper">
              <div class="list-column">
                <h3 class="list-head list-head--green">Found Publications</h3>
                <ul class="list list--found">
                  <li v-for="(pub, index) in foundPublications" :key="index">
                    <span class="list-title">{{ pub.title }}</span>
                  </li>
                </ul>
              </div>
              <div class="list-separator"></div>
              <div class="list-column">
                <h3 class="list-head list-head--red">Not Found Publications</h3>
                <ul class="list list--notfound">
                  <li v-for="(pub, index) in notFoundPublications" :key="index">
                    <span class="list-title">{{ pub.title }}</span>
                    <div class="cbox-wrapper">
                      <input type="checkbox" v-model="pub.checked"
                        @change="updateNotFoundPublications(pub, this.localCandidates[this.localIndex].candidate._id)">
                      <span class="checkmark"></span>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
            <div class="dialog-actions">
              <button class="submit-button submit-button--small" @click="closeDialog">Cancel</button>
              <button class="submit-button submit-button--small" @click="closeDialog" type="submit">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';

export default {
  name: 'CandidatesTable',
  props: {
    candidates: {
      type: Array,
      required: true,
    },
    jobTitle: {
      type: String
    },
    jobDescription: {
      type: String
    },
    ranking: {
      type: Array
    }
  },
  data() {
    return {
      localCandidates: [...this.candidates],
      showPublications: false,
      totalArticles: 0,
      totalConference: 0,
      localCandidate: {},
      localIndex: 0,
      NotFoundPublications: [],
      localRanking: []
    };
  },
  methods: {
    showDialog(text) {
      this.$store.dispatch('showDialog', text);
    },
    showSpinner(text) {
      this.$store.dispatch('showSpinner', text);
    },
    hideSpinner() {
      this.$store.dispatch('hideSpinner');
    },
    updateSharedRanking() {
      this.$emit('updateRanking', this.localRanking);
    },
    updateNotFoundPublications(pub, id) {
      if (pub.checked) {
        this.NotFoundPublications.push({ pub, id });
      } else {
        const index = this.NotFoundPublications.indexOf(pub);
        if (index !== -1) {
          this.NotFoundPublications.splice(index, 1);
        }
      }
    },
    candidateForm(event) {
      event.preventDefault()
      //TODO
    },
    publicationEdit({ index }) {
      this.localIndex = index
      this.showPublications = true;
    },
    candidateEditUrl({ id }) {
      const inputRow = document.getElementById(id)
      inputRow.classList.toggle('active')
    },
    //Sending the new Url of the Candidate to the 
    saveUrl({ id }) {
      this.showSpinner("Waiting to find the data of the Candidate.It will take some time.")

      const inputRow = document.getElementById(id);
      const inputElement = inputRow.querySelector('.candidate-url');
      const inputValue = inputElement.value;
      console.log(inputValue);

      const parts = id.split('-');
      const index = parts[parts.length - 1];
      console.log(index);

      inputRow.classList.remove('active')
      this.loading = true;
      const formData = new FormData();

      formData.append('url', inputValue);
      formData.append('_id', this.candidates[index].candidate._id);

      axios.post('http://127.0.0.1:8000/api-endpoint/Url', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          this.hideSpinner()
          if (!response.data.candidate) {
            this.showErrorPopup = true;
            this.showDialog("Something went wrong with the Request.")
          } else {
            this.localCandidates[index] = response.data.candidate;
            console.log(response.data.candidate);
            this.showDialog("The Profile of the Candidate was found.")
          }
        })
        .catch(error => {
          this.hideSpinner();
          this.showDialog("We had an unexpected error:" + error.response.data.message);
        });
    },
    submitCandidates() {
      this.showSpinner("We are calculating the Ranking of the Candidates.It will take some time.");

      const formData = new FormData();
      formData.append('NotFoundPublications', JSON.stringify(this.NotFoundPublications))
      formData.append('candidates', JSON.stringify(this.localCandidates))
      formData.append('jobTitle', this.jobTitlejobTitle);
      formData.append('jobDescription', this.jobDescription);

      axios.post('http://127.0.0.1:8000/api-endpoint/RankingCandidates', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          this.hideSpinner();

          if (!response.data.rankings) {
            this.showErrorPopup = true;
            this.showDialog("Something went wrong")
          } else {
            this.localRanking = response.data.rankings;
            this.updateSharedRanking();
            this.showDialog("The Ranking Results are calculated.")
          }
        })
        .catch(error => {
          this.hideSpinner();
          this.showDialog("We had an unexpected error:" + error.response.data.message);
        });
    },
    closeDialog() {
      this.showPublications = false
    }
  },
  mounted() {
    this.showPublications - false;
    this.localCandidates.forEach(candidate => {
      candidate.candidate.publication.forEach(pub => {
        pub.checked = pub.researchgate_url || pub.googlescholar_url ? true : false;
      });
    });
  },
  computed: {
    foundPublications: function () {
      return this.localCandidates[this.localIndex].candidate.publication.filter(pub => pub.researchgate_url != '' || pub.googlescholar_url != '')
    },
    notFoundPublications: function () {
      return this.localCandidates[this.localIndex].candidate.publication.filter(pub => pub.researchgate_url == '' && pub.googlescholar_url == '')
    }
  }
}
</script>

<style src="./CandidatesTable.css"></style>
