# Helm package for Fedora

See Helm project here: https://tytel.org/helm/

This repository is based on [metal3d's earlier package]{https://github.com/metal3d/fedora-helm} and is used to generate the Copr repo [teervo/helm-synth]{https://copr.fedorainfracloud.org/coprs/teervo/helm-synth/}.

To install, first enable the repository
```
sudo dnf copr enable teervo/helm-synth
```

To install the standalone synth, run
```
sudo dnf install helm-synth
```

To install the LV2 plugin,
```
sudo dnf install lv2-helm-synth
```

To install the VST plugin,
```
sudo dnf install vst-helm-synth
```
