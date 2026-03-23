import { createRouter, createWebHistory } from "vue-router";
import DefaultView from "../views/DefaultView.vue";
import VoiceChatView from "../views/VoiceChatView.vue";

const routes = [
  {
    path: "/",
    name: "Default",
    component: DefaultView,
  },
  {
    path: "/voice",
    name: "VoiceChat",
    component: VoiceChatView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
