<template>
  <div class="tab-content" id="ranking-tab-content">
    <h2>Final Candidate Rating</h2>
    <hr />
    <table class="candidates-table">
      <thead>
          <tr>
            <td>Rank</td>
            <td>Name</td>
            <td>Score</td>
          </tr>
      </thead>
      <tbody>
        <tr v-for="(result, index) in results" :key="index">
          <td>{{ index + 1 }}</td>
          <td>{{ result.author }}</td>
          <td>{{ result.score }}</td>
        </tr>
      </tbody>
    </table>
  </div> 
</template>
  
<script>
export default {
  name:'RankingCandidates',
  props: {
    results: {
      type: Array,
      required: true,
    },
  },
  methods: {
  }
}
</script>

<style src="./CandidatesTable.css"></style>

