// Phase 1.7 Stage D hotfix: /sandbox is the prospect-facing URL referenced
// from the cold email and Vidyard script. Behavior is identical to the
// root route — same component, same query-param handling, same loadPrebaked
// flow. Re-export rather than duplicate so future Stage D/E/F changes to
// the home page propagate to the sandbox URL automatically.
export { default } from './index';
