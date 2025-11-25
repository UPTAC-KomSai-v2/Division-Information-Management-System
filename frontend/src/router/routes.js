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
      { path: 'repository', component: () => import('src/pages/RepositoryPage.vue') },
      { path: 'calendar', component: () => import('src/pages/CalendarPage.vue') },
      { path: 'services', component: () => import('src/pages/TicketsPage.vue') },
      { path: 'document', component: () => import('src/pages/DocumentsPage.vue') },
      { path: 'settings', component: () => import('src/pages/SettingsPage.vue') }
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
]

export default routes