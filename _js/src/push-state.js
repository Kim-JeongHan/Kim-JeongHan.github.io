// Copyright (c) 2017 Florian Klampfer
// Licensed under MIT

/*
eslint-disable
no-param-reassign,
import/no-extraneous-dependencies,
import/no-unresolved,
import/extensions
*/

import { fromEvent, zipWith } from 'rxjs';

import {
  catchError as recover,
  tap as effect,
  debounceTime,
  exhaustMap,
  filter,
  map,
  mergeMap,
  pairwise,
  share,
  startWith,
  switchMap,
  takeUntil,
} from 'rxjs/operators';

import elemDataset from 'elem-dataset';

import { hasFeatures, animate } from './common';
import CrossFader from './cross-fader';
import upgradeMathBlocks from './katex';

import Flip from './flip/flip';
import './flip/title';

class PushState {
  // eslint-disable-next-line class-methods-use-this
  startHistory() {}
}

const REQUIREMENTS = [
  'eventlistener',
  'queryselector',
  'requestanimationframe',
  'classlist',
  'documentfragment',
  'history',
  'opacity',
  'cssanimations',
];

const DURATION = 250;
const FADE_DURATION = 500;

// whenever the source observable encounters an error,
// we log it to the console, but continue as if it never happend
function makeUnstoppable() {
  return recover((error, caught) => {
    console.error(error); // eslint-disable-line
    return caught;
  });
}

if (!window.disablePushState && hasFeatures(REQUIREMENTS)) {
  const ua = navigator.userAgent.toLowerCase();
  const isSafari = ua.indexOf('safari') > 0 && ua.indexOf('chrome') < 0;

  const crossFader = new CrossFader({ duration: FADE_DURATION });

  const pushState = document.getElementById('_yPushState');

  const animationMain = document.createElement('div');
  animationMain.classList.add('animation-main');
  animationMain.classList.add('fixed-top');
  animationMain.innerHTML = `
    <div class="content">
      <div class="page"></div>
    </div>`;
  pushState.parentNode.insertBefore(animationMain, pushState);

  const loading = document.createElement('div');
  loading.classList.add('loading');
  loading.innerHTML = `
    <span class="sr-only">Loading...</span>
    <div class="sk-folding-cube">
      <div class="sk-cube1 sk-cube"></div>
      <div class="sk-cube2 sk-cube"></div>
      <div class="sk-cube4 sk-cube"></div>
      <div class="sk-cube3 sk-cube"></div>
    </div>
  `;
  document.querySelector('.navbar .content').appendChild(loading);

  const start$ = fromEvent(pushState, 'y-push-state-start').pipe(
    map(({ detail }) => detail),
    map((detail) => [detail, document.getElementById('_main')]),
    effect(() => {
      // If a link on the drawer has been clicked, close it
      if (!window.isDesktop && window.drawer.opened) {
        window.drawer.close();
      }
    }),
    share(),
  );

  const ready$ = fromEvent(pushState, 'y-push-state-ready').pipe(
    map(({ detail }) => detail),
    share(),
  );

  const progress$ = fromEvent(pushState, 'y-push-state-progress').pipe(
    map(({ detail }) => detail),
    // share()
  );

  const after$ = fromEvent(pushState, 'y-push-state-after').pipe(
    map(({ detail }) => detail),
    share(),
  );

  // const error$ = fromEvent(pushState, 'y-push-state-error');

  // HACK
  if (isSafari) {
    fromEvent(window, 'popstate')
      .subscribe(() => { document.body.style.minHeight = '999999px'; });

    after$
      .subscribe(() => { document.body.style.minHeight = ''; });
  }

  // FLIP animation (when applicable)
  start$.pipe(
    switchMap(([detail]) => {
      const { event: { currentTarget } } = detail;

      const flip = Flip.create(currentTarget.getAttribute
        && currentTarget.getAttribute('data-flip'), {
        animationMain,
        currentTarget,
        duration: DURATION,
      });

      // HACK: This assumes knowledge of the internal rx pipeline.
      // Could possibly be replaced with `withLatestFrom` shinanigans,
      // but it's more convenient like that.
      detail.flip = flip;

      return flip.start(currentTarget);
    }),
    makeUnstoppable(),
  ).subscribe();

  // Fade main content out
  start$.pipe(
    effect(([, main]) => { main.style.opacity = 0; }),
    filter(([{ type }]) => type === 'push' || !isSafari),
    exhaustMap(([{ type }, main]) => animate(main, [
      { opacity: 1 },
      { opacity: 0 },
    ], {
      duration: DURATION,
      // easing: 'ease',
      easing: 'cubic-bezier(0,0,0.32,1)',
    }).pipe(
      effect(() => { if (type === 'push') window.scroll(0, 0); }),
      zipWith(after$),
    )),
    makeUnstoppable(),
  ).subscribe();

  // Show loading bar when taking longer than expected
  progress$.pipe(
    effect(() => { loading.style.display = 'block'; }),
    makeUnstoppable(),
  ).subscribe();

  // TODO: error message!?
  // error$
  //   // .delay(DURATION) // HACK
  //   .do(() => {
  //     loading.style.display = 'none';
  //   })
  //   .subscribe();

  // Prepare showing the new content
  ready$.pipe(
    effect(() => { loading.style.display = 'none'; }),
    filter(({ type }) => type === 'push' || !isSafari),
    switchMap(({ flip, content: [main] }) => flip.ready(main).pipe(takeUntil(start$))),
    makeUnstoppable(),
  ).subscribe();

  ready$.pipe(
    switchMap(({ content: [main] }) => (
      crossFader.fetchImage(elemDataset(main)).pipe(takeUntil(start$))
    )),
    startWith(document.querySelector('.sidebar-bg')),
    pairwise(),
    mergeMap(crossFader.crossFade.bind(crossFader)),
    makeUnstoppable(),
  ).subscribe();

  // Animate the new content
  after$.pipe(
    filter(({ type }) => type === 'push' || !isSafari),
    map((kind) => [kind, document.querySelector('main')]),
    switchMap(([, main]) => animate(main, [
      { transform: 'translateY(-2rem)', opacity: 0 },
      { transform: 'translateY(0)', opacity: 1 },
    ], {
      duration: DURATION,
      // easing: 'ease',
      easing: 'cubic-bezier(0,0,0.32,1)',
    })),
    makeUnstoppable(),
  ).subscribe();

  after$.pipe(
    // Don't send a pageview when the user blasts through the history..
    debounceTime(2 * DURATION),
    effect(() => {
      // Send google analytics pageview
      if (window.ga) window.ga('send', 'pageview');

      // Upgrade math blocks
      upgradeMathBlocks();
    }),
    makeUnstoppable(),
  ).subscribe();

  new PushState(pushState, {
    replaceIds: ['_main'],
    linkSelector: 'a[href^="/"]',
    scriptSelector: 'script:not([type^="math/tex"])',
    duration: DURATION,
    noPopDuration: isSafari,
    scrollRestoration: !isSafari,
  }).startHistory();
}
