
var profile_vue = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app_profile',
    vuetify: new Vuetify(),
    data() {
        return {
            user: null,
            posts: null,
            friends: null,
            time: '',
        loading: true,
            errored: false
        }
    },
    components:{
        //'postFunction': postFunction,
    },
    methods: {
        // API(GET): Used to get user profile
        getProfile: function () {
            var url = 'http://127.0.0.1:8000/api/v1/profile/' + userid + '/'
            axios
                .get(url)
                .then(response => {
                    if (response.status == 200) {
                        this.user = response.data
                        this.errored = false
                        this.loading = false
                    }
                    else {
                        this.errored = true
                        this.loading = false
                    }
                })
                .catch(error => {
                    console.log(error)
                    this.errored = true
                })
                .finally(() => {
                    this.loading = false
                })
        },

        // API(GET): Used to get user posts
        getPosts: function () {
            var url = 'http://127.0.0.1:8000/api/v1/post/user'
            axios
                .get(url)
                .then(response => {
                    if (response.status == 200) {
                        this.posts = response.data
                        this.errored = false
                        this.loading = false
                    }
                    else {
                        this.errored = true
                        this.loading = false
                    }
                })
                .catch(error => {
                    console.log(error)
                    this.errored = true
                })
                .finally(() => {
                    this.loading = false
                })
        },

        // API(GET): Used to get user friends
        getFriends: function () {
            var url = 'http://127.0.0.1:8000/api/v1/friends/public/' + userid
            axios
                .get(url)
                .then(response => {
                    if (response.status == 200) {
                        this.friends = response.data
                        this.errored = false
                        this.loading = false
                    }
                    else {
                        this.errored = true
                        this.loading = false
                    }
                })
                .catch(error => {
                    console.log(error)
                    this.errored = true
                })
                .finally(() => {
                this.loading = false
                })
        }
    },
    filters: {
    },
    watch: {
        // Everytime a new date is picked, fetch the time slots for that date
        date_picker: function (value) {
            this.getTimeSlots()
        },
    },
    mounted() {
        this.getProfile();
        this.getFriends();
    },
})