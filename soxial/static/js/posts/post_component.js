Vue.component('post-function', {
    delimiters: ["[[", "]]"],
    data: function () {
      return {
        posts: null,
        errored: false,
        loading: true,
      }
    },
    methods: {
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
        },
    },
    mounted() {
        this.getPosts();
    },
});