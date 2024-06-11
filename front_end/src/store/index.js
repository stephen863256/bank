import Vuex from 'vuex'
import {SET_USER, CLEAR_USER,SET_ROLES,CLEAR_ROLES} from './types'


const store = new Vuex.Store({
    state: {
        user: null,
        roles: [],
        isLoggedIn: false,  // 添加这一行
    },
    getters: {
        getUser(state) {
            return state.user == null ? "" : state.user
        },
        getRoles(state) {
            return state.roles
        },
        isLoggedIn(state) {
            return state.isLoggedIn
        }
    },
    mutations: {
        [SET_USER](state, user) {
            state.user = user;
            state.isLoggedIn = true; 
        },
        [CLEAR_USER](state) {
            console.log("clear user");
            state.user = null;
            state.isLoggedIn = false; 
        },
        [SET_ROLES](state, user) {
            console.log("user", user); 
            if(user.username == "admin") {
                state.roles = ["admin"];
            } else {
                state.roles = ["user"];
            }
        },
        [CLEAR_ROLES](state) {
            state.roles = [];
        }
    },
    actions:{
        setUser({commit}, user) {
            commit(SET_USER, user);
            commit(SET_ROLES, user);
        },
        clearUser({commit}) {
            commit(CLEAR_USER);
            commit(CLEAR_ROLES);
        }
    }
})

export default store