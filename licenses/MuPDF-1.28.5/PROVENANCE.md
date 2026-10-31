# MuPDF 1.28.5 bundled components: license file provenance

PyMuPDF 2.0 (pymupdf_git_sha 7db0ab090698d49de637046786c8f85f29d89fd2) is built on MuPDF 1.28.5
(tag commit 8ad45e92f0935d3d87f1db3f873086472a5e1b24). The files in this folder were copied verbatim
from that tag and from the submodule commits it pins, limited to the components that the Windows
build (platform/win32/libmupdf.vcxproj and the projects it references) compiles into mupdfcpp64.dll.

Not compiled into the DLL and therefore not included: curl, freeglut, OpenSSL (libpkcs7 without libcrypto).
The AGPL-3.0 text used by MuPDF, jbig2dec and extract is identical; it is kept once as COPYING.
FreeType is dual-licensed (FTL or GPLv2); this distribution uses it under the FTL.

## Submodule commits (MuPDF 1.28.5)

- brotli: https://github.com/ArtifexSoftware/thirdparty-brotli @ 2523f3314501aa5c90e561922b2e668b3ccee26e
- cmark-gfm: https://github.com/ArtifexSoftware/thirdparty-cmark-gfm @ 74e0f5b6b62bbdd1e262c92f4bb2c6c871c6307e
- extract: https://github.com/ArtifexSoftware/extract @ 8750ac39c30a0d65119b426b5a491c5b8e8bf674
- freetype: https://github.com/ArtifexSoftware/thirdparty-freetype2 @ 0a0221a1347e2f1e07c395263540026e9a0aa7c7
- gumbo-parser: https://github.com/ArtifexSoftware/thirdparty-gumbo-parser @ 61bd4e736c3b342e592f65be0d65ec6a0acd8dcb
- harfbuzz: https://github.com/ArtifexSoftware/thirdparty-harfbuzz @ c28ba35a1e6dc4b6b32e2b1d11fd2a408f6c86bb
- jbig2dec: https://github.com/ArtifexSoftware/jbig2dec @ dc15c39bbbddc90f79c14563d2eb5a794106be8f
- lcms2: https://github.com/ArtifexSoftware/thirdparty-lcms2 @ d69c64417c4a33a4629957fc0e08f4f4c5abcc3d
- leptonica: https://github.com/ArtifexSoftware/thirdparty-leptonica @ 7fbe9ea76d1e0c48a02b2ed371d24f92c7bac40c
- libjpeg: https://github.com/ArtifexSoftware/thirdparty-libjpeg @ 627faae398468d5d11e3d694dc325432f734b5c4
- mujs: https://github.com/ArtifexSoftware/mujs @ 2c61a7bed7e7625c03c6e82e644a711ac4471c1e
- openjpeg: https://github.com/ArtifexSoftware/thirdparty-openjpeg @ 957029eb875eee1118743f200cb86da9d8289de2
- tesseract: https://github.com/ArtifexSoftware/thirdparty-tesseract @ ad0f76d971946512a62c933f490c8111877eddaa
- zint: https://github.com/ArtifexSoftware/thirdparty-zint @ 7a9fdd6cd00cd5bfd0082705d934c13ef84f25e1
- zlib: https://github.com/ArtifexSoftware/thirdparty-zlib @ da607da739fa6047df13e66a2af6b8bec7c2a498
- zxing-cpp: https://github.com/ArtifexSoftware/thirdparty-zxing-cpp @ 742aef959e12a41eda494df78fd567c2e715ff57

## Files

| File | Source | SHA-256 |
|---|---|---|
| COPYING | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/COPYING | 57c8ff33c9c0cfc3ef00e650a1cc910d7ee479a8bc509f6c9209a7c2a11399d6 |
| README | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/README | f90e04c2dece024ca0b2acb3e3c8a8d48c2e9b281cf01520922e15e3684869d5 |
| thirdparty/jbig2dec/LICENSE | https://github.com/ArtifexSoftware/jbig2dec/blob/dc15c39bbbddc90f79c14563d2eb5a794106be8f/LICENSE | 1bf5258afe453934484fd0cea97508b72301633a6a78b0ae8a9ee44ac78f26d9 |
| thirdparty/mujs/COPYING | https://github.com/ArtifexSoftware/mujs/blob/2c61a7bed7e7625c03c6e82e644a711ac4471c1e/COPYING | 0ca9b4fbfbcab8ac7d32475890d866efc02f4cffb6b6da5c0e9a0615cc3d82fe |
| thirdparty/freetype/LICENSE.TXT | https://github.com/ArtifexSoftware/thirdparty-freetype2/blob/0a0221a1347e2f1e07c395263540026e9a0aa7c7/LICENSE.TXT | bd36c8b474855fa294c2ec5c184544478ef3720aad37d65a6296a4f264fd2d3b |
| thirdparty/freetype/FTL.TXT | https://github.com/ArtifexSoftware/thirdparty-freetype2/blob/0a0221a1347e2f1e07c395263540026e9a0aa7c7/docs/FTL.TXT | 5a5ee54c5001bbad1cdc1a57cc3dd4c42199b2da09d39c7ee41fab002d02967f |
| thirdparty/gumbo-parser/COPYING | https://github.com/ArtifexSoftware/thirdparty-gumbo-parser/blob/61bd4e736c3b342e592f65be0d65ec6a0acd8dcb/COPYING | c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4 |
| thirdparty/harfbuzz/COPYING | https://github.com/ArtifexSoftware/thirdparty-harfbuzz/blob/c28ba35a1e6dc4b6b32e2b1d11fd2a408f6c86bb/COPYING | ba8f810f2455c2f08e2d56bb49b72f37fcf68f1f4fade38977cfd7372050ad64 |
| thirdparty/libjpeg/README | https://github.com/ArtifexSoftware/thirdparty-libjpeg/blob/627faae398468d5d11e3d694dc325432f734b5c4/README | 913af09f785683accdf660b85dcf27fdd567d4ad649daa95cb8771b040db79d1 |
| thirdparty/lcms2/LICENSE | https://github.com/ArtifexSoftware/thirdparty-lcms2/blob/d69c64417c4a33a4629957fc0e08f4f4c5abcc3d/LICENSE | 74fe8934cee0e63e8368d4a6b3a703b603e753a62b75b75273572e98a57ebf75 |
| thirdparty/openjpeg/LICENSE | https://github.com/ArtifexSoftware/thirdparty-openjpeg/blob/957029eb875eee1118743f200cb86da9d8289de2/LICENSE | a6af136f3e15038a666b61f376612a07d9a4e48cb7c01adbf3e33b3f14ab49b6 |
| thirdparty/zlib/LICENSE | https://github.com/ArtifexSoftware/thirdparty-zlib/blob/da607da739fa6047df13e66a2af6b8bec7c2a498/LICENSE | e32ff4e00d9d94930537635291da39e7e612703334bf6fde8c7f1686fe8a45a2 |
| thirdparty/tesseract/LICENSE | https://github.com/ArtifexSoftware/thirdparty-tesseract/blob/ad0f76d971946512a62c933f490c8111877eddaa/LICENSE | cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30 |
| thirdparty/leptonica/leptonica-license.txt | https://github.com/ArtifexSoftware/thirdparty-leptonica/blob/7fbe9ea76d1e0c48a02b2ed371d24f92c7bac40c/leptonica-license.txt | 87829abb5bbb00b55a107365da89e9a33f86c4250169e5a1e5588505be7d5806 |
| thirdparty/zxing-cpp/LICENSE | https://github.com/ArtifexSoftware/thirdparty-zxing-cpp/blob/742aef959e12a41eda494df78fd567c2e715ff57/LICENSE | c6596eb7be8581c18be736c846fb9173b69eccf6ef94c5135893ec56bd92ba08 |
| thirdparty/zint/LICENSE | https://github.com/ArtifexSoftware/thirdparty-zint/blob/7a9fdd6cd00cd5bfd0082705d934c13ef84f25e1/LICENSE | d69af7f2442fcde1c3372cbbb43907fa1f4b3a91ef3899be69dd3a726dc255a4 |
| thirdparty/brotli/LICENSE | https://github.com/ArtifexSoftware/thirdparty-brotli/blob/2523f3314501aa5c90e561922b2e668b3ccee26e/LICENSE | 3d180008e36922a4e8daec11c34c7af264fed5962d07924aea928c38e8663c94 |
| thirdparty/cmark-gfm/COPYING | https://github.com/ArtifexSoftware/thirdparty-cmark-gfm/blob/74e0f5b6b62bbdd1e262c92f4bb2c6c871c6307e/COPYING | c22e885f33b821bddb24cf007145e5540655b6c0f403e49e6c76a93c28e6d9a9 |
| fonts/urw/OFL.txt | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/fonts/urw/OFL.txt | 3b709798a0943cbf824ed21b6b2c735e482cf6cb8fa11441e57381c2650253ca |
| fonts/noto/COPYING | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/fonts/noto/COPYING | 6a73f9541c2de74158c0e7cf6b0a58ef774f5a780bf191f2d7ec9cc53efe2bf2 |
| fonts/han/LICENSE.txt | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/fonts/han/LICENSE.txt | 6a73f9541c2de74158c0e7cf6b0a58ef774f5a780bf191f2d7ec9cc53efe2bf2 |
| fonts/han/README.txt | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/fonts/han/README.txt | dd6d50b8f1ba504ba2d4f38911c907fcc5f0753cd4942f52c3a991a57931e564 |
| fonts/sil/OFL.txt | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/fonts/sil/OFL.txt | 73dfe0817e50210df5ee60d551515b9ebef9156522e45d166ca5f0a2456f1f39 |
| fonts/sil/README.txt | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/fonts/sil/README.txt | 3b0fd4e92a4c99fca8d2da978f5f26ca2488fd999d1fa33af770c6e0114f5216 |
| fonts/droid/NOTICE | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/fonts/droid/NOTICE | 38751245389e1e23f73e6f5384b5cbe7fa972cc4410c5adc9c04b082a0b9561a |
| hyphen/README | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/README | e0e651866f66d910ad2f9b9b228ae7ed7fc94ee25e0823cc9b2391576e2b22c4 |
| hyphen/license/hyph-af.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-af.info | 1957654979e56e9b77add085430b443bd3217cfa30943a1f293e05f9e88e2c3e |
| hyphen/license/hyph-as.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-as.info | feba53b46eff57eddf04d6cd0639bb59b56a5d6ae38b1e9b5d1c25a4063a8248 |
| hyphen/license/hyph-be.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-be.info | 58354164feabcef3efe156970712c0818a9c8ffee998c4562b6620fe80cd1612 |
| hyphen/license/hyph-bg.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-bg.info | 06c651f77ec4ce0d507a225b46c3e52fa1a275f6f65f4e3360e37678ea45e4f5 |
| hyphen/license/hyph-bn.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-bn.info | 75e30a3270421007219d277353b13a72c8f925a2b89f16ce5361d82f58ac8437 |
| hyphen/license/hyph-ca.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-ca.info | 4a2a2af321330525022c962bb16ab2e2c56512c37cc4f7e7e1467ce9be2822d9 |
| hyphen/license/hyph-cop.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-cop.info | 87891f2e290276a3614b35eb0642071eb34baab4046f56d974bc5841c00423cc |
| hyphen/license/hyph-da.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-da.info | 57c58ab01b16cfde961fd45b3e466ad373e8b58504648ff8ff417a82b5ec6480 |
| hyphen/license/hyph-de-1996.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-de-1996.info | aad8cc43d41f225e3770475c959f47594b54f780712931aa4f10090bce545d70 |
| hyphen/license/hyph-el-polyton.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-el-polyton.info | eb429c009b4fbfa8568ef19ec05c9066c3264f814251105be88f6cc91c831e68 |
| hyphen/license/hyph-en-us.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-en-us.info | 3296b50a85819db4a81d0983a4197fa5139ef931365ea76a13529a7e762128d3 |
| hyphen/license/hyph-es.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-es.info | 844cb3e361c4b0d1bd61c31123eb8724753e28ddfe28523106ccd91ee02ad486 |
| hyphen/license/hyph-et.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-et.info | 644d6ea2cd5801b67a7d97e14dbd691915cd8e1f75486f9d79bf67b23050c7b0 |
| hyphen/license/hyph-fi.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-fi.info | 49e8d96053c4abd893f815424cc88fb812bbb71900c08c1fa6dcaa5281a3ee02 |
| hyphen/license/hyph-fr.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-fr.info | d66c5b505f330f0f29c9a61c97d0cb5c5f3004d41a29a0435056854d28c18846 |
| hyphen/license/hyph-gu.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-gu.info | 5f87d3a0775a263579c2fecf5d006eacc664f3b0f3824a5e2f8de9942e2c0124 |
| hyphen/license/hyph-hi.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-hi.info | d3452642fb44c3e6a5f5b788acd5a4333b560bf1250daa92c1bf7d7190d76dd0 |
| hyphen/license/hyph-hr.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-hr.info | ccbc3fcd98d5d21a524f94d9bc705f64fded49782b76e9277f61f996874bbac1 |
| hyphen/license/hyph-hu.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-hu.info | 103b6a4611f931c3523afee980c81c49c1b3f905dd7bc2ef2df08142f9add0fd |
| hyphen/license/hyph-hy.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-hy.info | 844484512560e53b6b646d901f832b5ec2597e61aada34760bb36b4054e915eb |
| hyphen/license/hyph-is.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-is.info | 3771dad6b76cbc7f6fcc79ad751da3768ce566d74cf9fc39cd428e3f50318c3b |
| hyphen/license/hyph-it.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-it.info | 7a3508434c511ad06fbddbd9463ea81f64ef916c33c6cd672dbbcc99f6d1f800 |
| hyphen/license/hyph-ka.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-ka.info | 097ebc0b6637546f2ac47dc16c45c08454d93fc10b7a02399a27972d4223228c |
| hyphen/license/hyph-kn.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-kn.info | c59f140fa0b885d6c6d9497948be4d26d801182f0cdc80d9a52c69ca64044a57 |
| hyphen/license/hyph-la.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-la.info | 801d8c49cb08d554d08e177f84579aec4211d25a3e4cc25902843ddcd1e4bedb |
| hyphen/license/hyph-lt.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-lt.info | 6e82ec7a36bbe58965f33146a3cb7c37167a525f793938d7aaa5b081ed60aa37 |
| hyphen/license/hyph-lv.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-lv.info | a5bfe75b2834d27db323d7a011497a168b89c54b90054d89cbb1232cd619172b |
| hyphen/license/hyph-ml.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-ml.info | 6cec9aa039fbb55855dde2b3b8b47b11fa965903e78ca3af64b0edd941fbc1cb |
| hyphen/license/hyph-mn-cyrl.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-mn-cyrl.info | f2ad505f2669ba1716c236594b72c05538a9bcb30fb2265e129e8b0417c40779 |
| hyphen/license/hyph-mr.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-mr.info | a09832fff4a5ec0e5ecd0fd858152e1bf2ef441ea3751ff9488d2c2f9b2618e7 |
| hyphen/license/hyph-nb.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-nb.info | c5308d6b843ac9298ae7ff5f4c28d31ebb0ba8914184b9e18202b675147bbcf6 |
| hyphen/license/hyph-nl.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-nl.info | f382780d756f13efdba0e913397afb91fddbb28534852381f7b97f93928c3a5c |
| hyphen/license/hyph-or.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-or.info | 600541fd8ef59a882f949367b3f08f2a10312daa16d5be17bf4084c27cf50e82 |
| hyphen/license/hyph-pa.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-pa.info | ba71ca37cda98f8fc85737cfa7eb691aa122fb3ba6fd7e40543076f57fae83ee |
| hyphen/license/hyph-pi.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-pi.info | 15da529646346f296bf51a76bc76b86a78457f6a48990270c723c56224699619 |
| hyphen/license/hyph-pl.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-pl.info | 3927b7c9364589d501f2eebbf4421be4f2d8cd4df13fcdc616b6b6000fad88dc |
| hyphen/license/hyph-pt.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-pt.info | befb02719155c9339ec831c30f4ed68204585d34b5d985603456f9c38d336aee |
| hyphen/license/hyph-ro.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-ro.info | 536a7ce30960fea3dfd7a4050ecb9564ca466e78acba75c2764a60d9d2d1372e |
| hyphen/license/hyph-ru.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-ru.info | 392c96dd05aec7d935fc9db7e98c2e90eb0a78bc43c1087fcf651ccb18b8cac1 |
| hyphen/license/hyph-sa.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-sa.info | a54cbc35c551d87169d5d6b3afa41806f3e3b8470dd9f0b0ccf11c16c3b8e6bf |
| hyphen/license/hyph-sl.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-sl.info | ab0a05c4fb61f3cf0a6c8829696e0c546ba4d07d0699312811af07db037f6db8 |
| hyphen/license/hyph-sq.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-sq.info | 2ff8550b54610755551add105cdf1eb2b92453fdda9e12f6ba7ce96db12edd4f |
| hyphen/license/hyph-sv.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-sv.info | f0db446c81d348e691457239b0250b521ab230aa80abd7b54066783e93ac7fe9 |
| hyphen/license/hyph-ta.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-ta.info | dcf9da99c1927600297de580c6dbf9c9d707c83cd946509fea720e7ead916197 |
| hyphen/license/hyph-te.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-te.info | 32db1869dc90ea826d4b6a3c4ca1b1e5b5cc1bfa0967bbc74d64ac5611516e20 |
| hyphen/license/hyph-th.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-th.info | dd2c5d1dc72327925ebaa901656cbb6badeaaee13f660e48096244fa81ce5eed |
| hyphen/license/hyph-tk.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-tk.info | 34d483f8d40572b8bda5f6b4ff1aee82710ab72fb78d7d5fa43cf6c2133cf205 |
| hyphen/license/hyph-tr.info | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/hyphen/license/hyph-tr.info | c9091880f8ba90990f66877a0f40b270ba9d10b91f9bb03d45ebfd2548b1daf7 |
| cmaps/README | https://github.com/ArtifexSoftware/mupdf/blob/1.28.5/resources/README | 5c64f502e6e352a4bef720b11f42f4dfbbf69eb61c89733582453ff7a5ce0533 |
| cmaps/cmap-resources-LICENSE.md | https://github.com/adobe-type-tools/cmap-resources/blob/4cc485e095d821e797d42d15604d08ed33d76b22/LICENSE.md | 742665db9c8e1bc72603c6d319ca3e90b83bd6d95202f0cd4ef11068a07a9c29 |
| cmaps/mapping-resources-pdf-LICENSE.txt | https://github.com/adobe-type-tools/mapping-resources-pdf/blob/97b0f5eecaaf4adad287f5c5b68f36af2bff84f4/LICENSE.txt | feb8b068a417681821823ef2e8995072aa111121fa11f8664038f78717f4497c |
