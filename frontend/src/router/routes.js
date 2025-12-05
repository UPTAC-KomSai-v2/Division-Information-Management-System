const routes = [
  {
    path: '/',
    redirect: '/login'
  },

  {
    path: '/app',
    redirect: '/app/dashboard',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'dashboard', component: () => import('src/pages/DashPage.vue') },
      { path: 'directory', component: () => import('src/pages/DirectoryPage.vue') },
      { path: 'calendar', component: () => import('src/pages/CalendarPage.vue') },
      { path: 'services', component: () => import('src/pages/TicketsPage.vue') },
      { path: 'documents', component: () => import('src/pages/DocumentsPage.vue') },
      { path: 'upload', component: () => import('src/pages/DocUploadPage.vue') },
      { path: 'profile', component: () => import('pages/UserProfilePage.vue') },
      { path: 'messages', component: () => import('src/pages/MessagesPage.vue') },
    ],
  },

  {
    path: '/login',
    component: () => import('src/pages/LoginPage.vue')
  },

  {
    path: '/forgot-password',
    component: () => import('src/pages/PSForgotPage.vue')
  },


  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },


  {
    path: '/app/admin',
    component: () => import('pages/AdminDashboard.vue'),
    meta: { requiresAdmin: true }
  },
]

export default routes
