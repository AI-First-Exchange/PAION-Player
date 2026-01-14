AI First Exchange (AIFX) Player

PAION Engine – Reference Implementation

The AI First Exchange (AIFX) Player is a cross-platform application for verifying, inspecting, and playing AI-generated music packaged in the AIFM (AI First Music Format).

This repository contains the PAION Player engine, which serves as the reference implementation for the AIFX ecosystem.

The application runs locally and launches a browser-based interface via localhost.

🌐 About AI First Exchange (AIFX)

AI First Exchange (AIFX) is an open, community-driven initiative developing transparent, integrity-verifiable, and future-proof file standards for AI-generated media.

AIFX standards enable creators, developers, platforms, and archivists to consistently document:

Human creative direction and authorship

Prompts and toolchains

Editing and selection steps

Provenance and verification status

Long-term archival integrity

AIFX is designed to function as a format-level provenance and authorship declaration layer, compatible with evolving legal, regulatory, and technical standards.

🔧 PAION Player (Engine)

PAION is the internal engine and development codename powering the AIFX Player.

PAION Player provides:

Local AIFM verification

Structured metadata inspection

Playback of embedded audio assets

Browser-based UI with no external services required

PAION is not the public-facing product brand.
The public standard and ecosystem are branded as AI First Exchange (AIFX).

🎵 Supported Format — AIFM

AIFM (AI First Music Format) is a ZIP-based container format designed to store AI-generated music alongside its provenance data.

An AIFM package may include:

Audio files (.wav, .mp3, etc.)

Prompts and generation context

Optional stems

Structured metadata

Authorship and verification fields

All metadata is stored in a standardized manifest.json.

🔍 Current Features (v0.1.0)

AIFM structure validation

Metadata inspection

Local playback via browser or system audio

Offline operation (no cloud dependencies)

This release is considered early-stage and evolving.

📦 Builds & Distribution

This repository provides the source code and reference implementation for transparency, standards compliance, and developer contribution.

Precompiled desktop applications and installers may be provided to supporters and early adopters to help fund ongoing development of the AI First Exchange (AIFX) ecosystem.

Until formal code signing and trademark registration are completed, distributed builds should be considered early-access and pre-certification.

🔗 Project home & updates:
https://paion.io

📜 Distribution & Licensing

This repository is source-available and provided for:

Transparency

Review and learning

Development and contribution

Compiled binaries, packaged applications, and installers are distributed separately to support ongoing development and maintenance.

Redistribution of compiled applications under the AIFX or PAION names in a way that implies official status is not permitted without permission.

For licensing or commercial inquiries:

📧 licensing@paion.io

(Email routing will be activated shortly. Until then, please use GitHub Issues or Discussions.)

🧭 Brand Usage & Forks

Anyone may implement the AIFX formats or build independent tools using the specifications.

Forks and modified versions of this software must not present themselves as the official AI First Exchange or imply endorsement, certification, or affiliation without permission.

This separation ensures clarity, trust, and interoperability across the ecosystem.

🏛️ Stewardship

AI First Exchange is an open standard guided by its original author and community contributors.

The goal of stewardship is to maintain clarity, interoperability, and long-term archival integrity — not to restrict innovation or ownership of creative works.

📛 Trademarks

AI First Exchange™ (AIFX™), PAION™, AIFM™, AIFI™, AIFV™, and AIFP™ are trademarks of Joseph Simon Simbulan.

Use of the source code does not grant permission to use these names or associated branding in a way that implies official status or endorsement.

All other product names, logos, and brands are property of their respective owners.

🤝 Contributing

Contributions, discussions, and feedback are welcome.

Please use GitHub Issues and Discussions to:

Report bugs

Propose enhancements

Discuss format evolution

Ask implementation questions

AI First Exchange (AIFX)

Creating a transparent, trustworthy future for AI media — one standard at a time.
