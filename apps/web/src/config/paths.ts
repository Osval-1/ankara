export const paths = {
  home: {
    getHref: () => '/',
  },

  auth: {
    register: {
      getHref: (redirectTo?: string | null | undefined) =>
        `/auth/register${redirectTo ? `?redirectTo=${encodeURIComponent(redirectTo)}` : ''}`,
    },
    login: {
      getHref: (redirectTo?: string | null | undefined) =>
        `/auth/login${redirectTo ? `?redirectTo=${encodeURIComponent(redirectTo)}` : ''}`,
    },
  },

  app: {
    root: {
      getHref: () => '/app',
    },
    dashboard: {
      getHref: () => '/app',
    },
    diagnose: {
      getHref: () => '/app/diagnose',
    },
    interactions: {
      getHref: () => '/app/interactions',
    },
    escalations: {
      getHref: () => '/app/escalations',
    },
    adviceTemplates: {
      getHref: () => '/app/advice-templates',
    },
    extensionWorkers: {
      getHref: () => '/app/extension-workers',
    },
    modelVersions: {
      getHref: () => '/app/model-versions',
    },
    users: {
      getHref: () => '/app/users',
    },
    profile: {
      getHref: () => '/app/profile',
    },
  },
} as const;
