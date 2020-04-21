# cb-terminal
A rebuild and redesign of the terminal interface used by the Chez Betty store 
at the University of Michigan. It is a native application running in Electron 
with logic handled in Vue. Installation and integration handled with the 
[vue-cli-plugin-electron-builder](https://github.com/nklayman/vue-cli-plugin-electron-builder) 
plugin. The UI was designed using the Bulma CSS framework.

## Things to be Added
Major:
- **HID support:** It being built on Node lets us use libraries like node-hid to get true HID
input with from each port. However, to do that we needed to have access to any of the
scanners we needed to build the interface for. It felt counterintuitive to attempt to do 
this without being able to test it at all, so we added function stubs where the code should
be able to be added at a later time.
- **Testing:** We were only able to test the interface with very limited database sizes running 
locally. In order to gauge performance and usability with a slower client / server connection
we'd need access to some subset of the actual CB databases, which was difficult with the quarantine.

Minor:
- **UI improvements:** We tried our best to fix some of the egregious faults with the current UI, like
its fixed size. That being said, there are definitely areas that could look much nicer with 
relatively minimal effort. Things like animations and transistions are quite painless if done
with Vue.
- **Interactivity:** More modal popups and interaction. We have quite a few modals already, but I'm sure there are a few 
contextual issues that could still use user explanation.


## Installation
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn electron:serve
```

### Compiles and minifies for production
```
yarn electron:build
```
