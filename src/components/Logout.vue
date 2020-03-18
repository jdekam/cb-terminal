<template>
  <div class="container">
    <div id="wrap">
      <div id="alerts" class="container"></div>
      <div id="content" class="container">
        <div class="row">
          <div class="col-md-12">
            <div class="row">
              <div class="col-md-12">
                <div class="jumbotron top">
                  <img class="pull-right" src="../assets/chezbetty_1000px.jpg" style="margin-top:5px;width:120px;" />
                  <h1>Chez Betty is Back!</h1>
                  <p>Welcome! Betty is the 24/7 food co-op for all members of the CSE community.</p>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-3">
                <div class="list-group">
                  <div class="list-group-item list-group-item-info list-group-item-header">Navigation</div>
                  <a href="/items" class="list-group-item">Item List</a>
                  <a href="http://127.0.0.1:6543/user/item/request" class="list-group-item">Request an Item</a>
                  <a href="/about" class="list-group-item">About</a>
                </div>
              </div>
              <div class="col-md-5"></div>
              <div class="col-md-4">
                <div class="panel panel-default">
                  <div class="panel-heading">
                    <h3 class="panel-title">You Are Logged In</h3>
                  </div>
                  <div class="panel-body">
                    <p>
                      To make a deposit and see your transactions,
                      go to your <a href="/user">user</a> page.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="navbar navbar-fixed-bottom" role="navigation">
        <div class="container-fluid">
          <hr />
          <p>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-en">English</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-de">Deutsch</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-fr">français</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-tw">漢語</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-cn">简体中文</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-fa">فارسی</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-ro">Română</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-es">Español</a>
            <a class="btn btn-default btn-lg btn-bordered" href="/lang-ar">العربية</a>
            <strong>Can you help translate Betty? github.com/cseg-michigan/chez-betty</strong>
          </p>
          <hr />
        </div>
      </div>
    </div>

    <!--
    <script src="http://127.0.0.1:6543/static/js/chezbetty-common-onload.js"></script>
    -->

    <!-- Google Analytics tracker -->
    <!--
    <script>
      (function(i, s, o, g, r, a, m) {
        i['GoogleAnalyticsObject'] = r;
        i[r] = i[r] || function() {
          (i[r].q = i[r].q || []).push(arguments)
        }, i[r].l = 1 * new Date();
        a = s.createElement(o),
          m = s.getElementsByTagName(o)[0];
        a.async = 1;
        a.src = g;
        m.parentNode.insertBefore(a, m)
      })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

      ga('create', 'UA-55624000-1', 'auto');
      ga('send', 'pageview');
    </script>
    -->

    <!--
    <link rel="stylesheet" type="text/css" href="http://127.0.0.1:6543/_debug_toolbar/static/toolbar/toolbar_button.css" />

    <div id="pDebug">
      <div id="pDebugToolbarHandle">
        <a title="Show Toolbar" id="pShowToolBarButton" href="http://127.0.0.1:6543/_debug_toolbar/313430353034333034353034303136" target="pDebugToolbar">&#171;</a>
      </div>
    </div>
  -->
  </div>
</template>

<style scoped>
@import '../assets/Logout.css';
</style>

<script>
import 'jquery'
import 'bootstrap'
import axios from 'axios'

export default {
  data() {
    return {
      debt: 'Loading',
      umid: '',
      scanned: false,
      announcements: [{
        content: "Placeholder announcement!",
      }, ],
    }
  },
  methods: {
    getAnnouncements() {
      const url = '/terminal_get_announcements/'
      axios.get(url).then(result => {
          this.announcements = result.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    getDebt() {
      const url = '/terminal_get_debt/'
      axios.get(url).then(result => {
          this.debt = result.data.debt
        })
        .catch(error => {
          console.log(error)
        })
    },
    checkUmid() {
      const url = '/terminal_check_umid/'
      axios.post(url, {
          umid: this.umid,
          scanned: this.scanned,
        })
        .then((response) => {
          this.$router.push({
            name: 'terminal',
            params: {
              umid: response.data.umid
            }
          })
        })
        .catch((error) => {
          console.log(error)
          // snackbar error message, clear keypad
        })
    },
  }
}
</script>
