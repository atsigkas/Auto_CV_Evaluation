<template>
  <div class="tab-content" id="ranking-tab-content">
    <div v-if="this.ranking.length>0">
      <table>
        <thead>
            <tr>
              <th>Rank</th>
              <th>Name</th>
              <th>Score</th>
            </tr>
        </thead>
        <tbody>
          <tr v-for="(ranking, index) in ranking" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ ranking.name }}</td>
            <td>{{ ranking.score }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
  
<script>
export default {
  name:'RankingCandidates',
  props: {
    ranking: {
      type: Array,
      required: true,
    }
  },
  methods: {
  }
}
</script>
