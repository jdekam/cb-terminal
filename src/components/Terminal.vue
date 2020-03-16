<template>
  <div class="row">
    <div class="col-md-2">
      <div class="row well">
        <img src="../assets/chezbetty_1000px.jpg" class="pull-left" style="margin-top:5px;width:100px;">
        <h4 class="pull-right" style="width: 100px;">{{ username }}</h4>
      </div>

      <div id="user-info-current-balance" class="row well balance-box">
        <h4> Your Current Balance </h4>
        <span class="current-formatted-balance">{{ balance }}</span>
      </div>

      <div id="user-info-new-balance" class="row well balance-box">
        <h4> Balance after Purchase or Deposit </h4>
        <span>{{ "user.balance|format_currency|safe" }}</span>
      </div>

      <div id="pool-info-current-balance" class="row well balance-box" style="display:none;">
        <h4> Selected Pool Balance </h4>
        <span></span>
      </div>

      <div id="user-balance" class="hidden">{{ "user.balance" }}</div>
      <div id="user-umid" class="hidden">{{ "user.umid" }}</div>
      <div id="user-role" class="hidden">{{ "user.role" }}</div>

      <!--
      {% for pool in purchase_pools %}
      <div id="pool-balance-{{ pool.id }}" class="hidden">{{ "pool.balance" }}</div>
      {% endfor %}
      -->

    </div>
  </div>
</template>

<style scoped>
  .cb-icon {
    width: 180px;
    height: 180px;
    vertical-align: middle;
    margin-right: 1em;
  }
  .cb-title {
    vertical-align: middle;
  }
</style>

<script>
//import axios from 'axios'
import 'bootstrap'

export default {
  data() {
    return {
      username: "Administrator",
      balance: "69.00",

      debt: '$1.00',
      umid: '',
      scanned: false,
      announcements: [
        {
          content: "This is an announcement!",
        },
        {
          content: "Hello there! Repay your damn debt!",
        },
      ],
    }
  },
  methods: {
    getUsername() {
      // api call to get username
    },
    getBalance() {
      // api call to get user's current balance
    },
    getAnnouncements() {
      // api call to retreive announcements
    },
    getDebt() {
      // api call to retreive user debt
    },
  }
}
</script>
