import functools
from numpy import array

coords_string = '7.8354600 -2.5458960 10.9760160 6.9282000 2.2511040 11.7869640 3.9177240 -1.2729480 13.5219120  3.9177240 -1.2729480 13.5219120 6.9282000 2.2511040 11.7869640 7.8354600 -2.5458960 10.9760160  6.9282000 2.2511040 11.7869640 7.8354600 -2.5458960 10.9760160 10.2567480 0.7867200 8.4301200  10.2567480 0.7867200 8.4301200 7.8354600 -2.5458960 10.9760160 6.9282000 2.2511040 11.7869640  6.9282000 2.2511040 11.7869640 2.4212880 3.3326160 13.5219120 3.9177240 -1.2729480 13.5219120  3.9177240 -1.2729480 13.5219120 2.4212880 3.3326160 13.5219120 6.9282000 2.2511040 11.7869640  7.8354600 -2.5458960 10.9760160 3.9177240 -1.2729480 13.5219120 4.2818640 -5.8934760 11.7869640 4.2818640 -5.8934760 11.7869640 3.9177240 -1.2729480 13.5219120 7.8354600 -2.5458960 10.9760160 10.2567480 0.7867200 8.4301200 10.2078120 -3.3167160 7.6176720 7.8354600 -2.5458960 10.9760160 7.8354600 -2.5458960 10.9760160 10.2078120 -3.3167160 7.6176720 10.2567480 0.7867200 8.4301200 8.7603120 5.3922960 8.4301200 6.9282000 2.2511040 11.7869640 10.2567480 0.7867200 8.4301200 10.2567480 0.7867200 8.4301200 6.9282000 2.2511040 11.7869640 8.7603120 5.3922960 8.4301200 6.9282000 2.2511040 11.7869640 4.8425760 6.6652320 10.9760160 2.4212880 3.3326160 13.5219120 2.4212880 3.3326160 13.5219120 4.8425760 6.6652320 10.9760160 6.9282000 2.2511040 11.7869640 3.9177240 -1.2729480 13.5219120 0.0000000 0.0000000 14.2511040 2.4212880 3.3326160 13.5219120 2.4212880 3.3326160 13.5219120 0.0000000 0.0000000 14.2511040 3.9177240 -1.2729480 13.5219120 4.2818640 -5.8934760 11.7869640 3.9177240 -1.2729480 13.5219120 -0.0000000 -4.1193480 13.5219120 -0.0000000 -4.1193480 13.5219120 3.9177240 -1.2729480 13.5219120 4.2818640 -5.8934760 11.7869640 7.8354600 -2.5458960 10.9760160 4.2818640 -5.8934760 11.7869640 7.8354600 -6.6652320 8.4301200 7.8354600 -6.6652320 8.4301200 4.2818640 -5.8934760 11.7869640 7.8354600 -2.5458960 10.9760160 10.2567480 0.7867200 8.4301200 11.7531840 -1.2729480 4.3107840 10.2078120 -3.3167160 7.6176720 10.2078120 -3.3167160 7.6176720 11.7531840 -1.2729480 4.3107840 10.2567480 0.7867200 8.4301200 7.8354600 -2.5458960 10.9760160 10.2078120 -3.3167160 7.6176720 7.8354600 -6.6652320 8.4301200 7.8354600 -6.6652320 8.4301200 10.2078120 -3.3167160 7.6176720 7.8354600 -2.5458960 10.9760160 8.7603120 5.3922960 8.4301200 4.8425760 6.6652320 10.9760160 6.9282000 2.2511040 11.7869640 6.9282000 2.2511040 11.7869640 4.8425760 6.6652320 10.9760160 8.7603120 5.3922960 8.4301200 8.7603120 5.3922960 8.4301200 10.2567480 0.7867200 8.4301200 11.2100640 3.6423720 4.5022200 11.2100640 3.6423720 4.5022200 10.2567480 0.7867200 8.4301200 8.7603120 5.3922960 8.4301200 4.8425760 6.6652320 10.9760160 0.0000000 7.2847440 11.7869640 2.4212880 3.3326160 13.5219120 2.4212880 3.3326160 13.5219120 0.0000000 7.2847440 11.7869640 4.8425760 6.6652320 10.9760160 3.9177240 -1.2729480 13.5219120 -0.0000000 -4.1193480 13.5219120 0.0000000 0.0000000 14.2511040 0.0000000 0.0000000 14.2511040 -0.0000000 -4.1193480 13.5219120 3.9177240 -1.2729480 13.5219120 2.4212880 3.3326160 13.5219120 0.0000000 0.0000000 14.2511040 -2.4212880 3.3326160 13.5219120 -2.4212880 3.3326160 13.5219120 0.0000000 0.0000000 14.2511040 2.4212880 3.3326160 13.5219120 4.2818640 -5.8934760 11.7869640 -0.0000000 -4.1193480 13.5219120 -0.0000000 -8.2386840 10.9760160 -0.0000000 -8.2386840 10.9760160 -0.0000000 -4.1193480 13.5219120 4.2818640 -5.8934760 11.7869640 4.2818640 -5.8934760 11.7869640 3.9177240 -9.5116320 8.4301200 7.8354600 -6.6652320 8.4301200 7.8354600 -6.6652320 8.4301200 3.9177240 -9.5116320 8.4301200 4.2818640 -5.8934760 11.7869640 11.2100640 3.6423720 4.5022200 10.2567480 0.7867200 8.4301200 11.7531840 -1.2729480 4.3107840 11.7531840 -1.2729480 4.3107840 10.2567480 0.7867200 8.4301200 11.2100640 3.6423720 4.5022200 11.7531840 -1.2729480 4.3107840 10.2567480 -5.8785120 4.3107840 10.2078120 -3.3167160 7.6176720 10.2078120 -3.3167160 7.6176720 10.2567480 -5.8785120 4.3107840 11.7531840 -1.2729480 4.3107840 10.2078120 -3.3167160 7.6176720 10.2567480 -5.8785120 4.3107840 7.8354600 -6.6652320 8.4301200 7.8354600 -6.6652320 8.4301200 10.2567480 -5.8785120 4.3107840 10.2078120 -3.3167160 7.6176720 8.7603120 5.3922960 8.4301200 4.8425760 6.6652320 10.9760160 6.3087720 8.6832840 7.6176720 6.3087720 8.6832840 7.6176720 4.8425760 6.6652320 10.9760160 8.7603120 5.3922960 8.4301200 8.7603120 7.9381800 4.3107840 8.7603120 5.3922960 8.4301200 11.2100640 3.6423720 4.5022200 11.2100640 3.6423720 4.5022200 8.7603120 5.3922960 8.4301200 8.7603120 7.9381800 4.3107840 4.8425760 6.6652320 10.9760160 2.4212880 9.9978600 8.4301200 0.0000000 7.2847440 11.7869640 0.0000000 7.2847440 11.7869640 2.4212880 9.9978600 8.4301200 4.8425760 6.6652320 10.9760160 2.4212880 3.3326160 13.5219120 0.0000000 7.2847440 11.7869640 -2.4212880 3.3326160 13.5219120 -2.4212880 3.3326160 13.5219120 0.0000000 7.2847440 11.7869640 2.4212880 3.3326160 13.5219120 -0.0000000 -4.1193480 13.5219120 -3.9177240 -1.2729480 13.5219120 0.0000000 0.0000000 14.2511040 0.0000000 0.0000000 14.2511040 -3.9177240 -1.2729480 13.5219120 -0.0000000 -4.1193480 13.5219120 0.0000000 0.0000000 14.2511040 -3.9177240 -1.2729480 13.5219120 -2.4212880 3.3326160 13.5219120 -2.4212880 3.3326160 13.5219120 -3.9177240 -1.2729480 13.5219120 0.0000000 0.0000000 14.2511040 -0.0000000 -4.1193480 13.5219120 -4.2818640 -5.8934760 11.7869640 -0.0000000 -8.2386840 10.9760160 -0.0000000 -8.2386840 10.9760160 -4.2818640 -5.8934760 11.7869640 -0.0000000 -4.1193480 13.5219120 4.2818640 -5.8934760 11.7869640 -0.0000000 -8.2386840 10.9760160 3.9177240 -9.5116320 8.4301200 3.9177240 -9.5116320 8.4301200 -0.0000000 -8.2386840 10.9760160 4.2818640 -5.8934760 11.7869640 3.9177240 -9.5116320 8.4301200 6.9282000 -9.5358480 4.5022200 7.8354600 -6.6652320 8.4301200 7.8354600 -6.6652320 8.4301200 6.9282000 -9.5358480 4.5022200 3.9177240 -9.5116320 8.4301200 11.2100640 3.6423720 4.5022200 11.7531840 -1.2729480 4.3107840 11.7531840 1.2729480 0.1914360 11.7531840 1.2729480 0.1914360 11.7531840 -1.2729480 4.3107840 11.2100640 3.6423720 4.5022200 11.7531840 -1.2729480 4.3107840 10.2567480 -5.8785120 4.3107840 11.2100640 -3.6423720 0.0000000 11.2100640 -3.6423720 0.0000000 10.2567480 -5.8785120 4.3107840 11.7531840 -1.2729480 4.3107840 10.2567480 -5.8785120 4.3107840 7.8354600 -6.6652320 8.4301200 6.9282000 -9.5358480 4.5022200 6.9282000 -9.5358480 4.5022200 7.8354600 -6.6652320 8.4301200 10.2567480 -5.8785120 4.3107840 4.8425760 6.6652320 10.9760160 2.4212880 9.9978600 8.4301200 6.3087720 8.6832840 7.6176720 6.3087720 8.6832840 7.6176720 2.4212880 9.9978600 8.4301200 4.8425760 6.6652320 10.9760160 6.3087720 8.6832840 7.6176720 8.7603120 7.9381800 4.3107840 8.7603120 5.3922960 8.4301200 8.7603120 5.3922960 8.4301200 8.7603120 7.9381800 4.3107840 6.3087720 8.6832840 7.6176720 8.7603120 7.9381800 4.3107840 11.2100640 3.6423720 4.5022200 10.2567480 5.8785120 0.1914360 10.2567480 5.8785120 0.1914360 11.2100640 3.6423720 4.5022200 8.7603120 7.9381800 4.3107840 0.0000000 7.2847440 11.7869640 2.4212880 9.9978600 8.4301200 -2.4212880 9.9978600 8.4301200 -2.4212880 9.9978600 8.4301200 2.4212880 9.9978600 8.4301200 0.0000000 7.2847440 11.7869640 0.0000000 7.2847440 11.7869640 -4.8425760 6.6652320 10.9760160 -2.4212880 3.3326160 13.5219120 -2.4212880 3.3326160 13.5219120 -4.8425760 6.6652320 10.9760160 0.0000000 7.2847440 11.7869640 -0.0000000 -4.1193480 13.5219120 -3.9177240 -1.2729480 13.5219120 -4.2818640 -5.8934760 11.7869640 -4.2818640 -5.8934760 11.7869640 -3.9177240 -1.2729480 13.5219120 -0.0000000 -4.1193480 13.5219120 -2.4212880 3.3326160 13.5219120 -6.9282000 2.2511040 11.7869640 -3.9177240 -1.2729480 13.5219120 -3.9177240 -1.2729480 13.5219120 -6.9282000 2.2511040 11.7869640 -2.4212880 3.3326160 13.5219120 -0.0000000 -8.2386840 10.9760160 -4.2818640 -5.8934760 11.7869640 -3.9177240 -9.5116320 8.4301200 -3.9177240 -9.5116320 8.4301200 -4.2818640 -5.8934760 11.7869640 -0.0000000 -8.2386840 10.9760160 -0.0000000 -8.2386840 10.9760160 3.9177240 -9.5116320 8.4301200 0.0000000 -10.7331240 7.6176720 0.0000000 -10.7331240 7.6176720 3.9177240 -9.5116320 8.4301200 -0.0000000 -8.2386840 10.9760160 3.9177240 -9.5116320 8.4301200 2.4212880 -11.5713000 4.3107840 6.9282000 -9.5358480 4.5022200 6.9282000 -9.5358480 4.5022200 2.4212880 -11.5713000 4.3107840 3.9177240 -9.5116320 8.4301200 11.7531840 1.2729480 0.1914360 11.7531840 -1.2729480 4.3107840 11.2100640 -3.6423720 0.0000000 11.2100640 -3.6423720 0.0000000 11.7531840 -1.2729480 4.3107840 11.7531840 1.2729480 0.1914360 10.2567480 5.8785120 0.1914360 11.2100640 3.6423720 4.5022200 11.7531840 1.2729480 0.1914360 11.7531840 1.2729480 0.1914360 11.2100640 3.6423720 4.5022200 10.2567480 5.8785120 0.1914360 11.2100640 -3.6423720 0.0000000 10.2567480 -5.8785120 4.3107840 8.7603120 -7.9381800 0.1914360 8.7603120 -7.9381800 0.1914360 10.2567480 -5.8785120 4.3107840 11.2100640 -3.6423720 0.0000000 10.2567480 -5.8785120 4.3107840 6.9282000 -9.5358480 4.5022200 8.7603120 -7.9381800 0.1914360 8.7603120 -7.9381800 0.1914360 6.9282000 -9.5358480 4.5022200 10.2567480 -5.8785120 4.3107840 2.4212880 9.9978600 8.4301200 4.8425760 10.7845800 4.3107840 6.3087720 8.6832840 7.6176720 6.3087720 8.6832840 7.6176720 4.8425760 10.7845800 4.3107840 2.4212880 9.9978600 8.4301200 6.3087720 8.6832840 7.6176720 4.8425760 10.7845800 4.3107840 8.7603120 7.9381800 4.3107840 8.7603120 7.9381800 4.3107840 4.8425760 10.7845800 4.3107840 6.3087720 8.6832840 7.6176720 6.9282000 9.5358480 0.0000000 8.7603120 7.9381800 4.3107840 10.2567480 5.8785120 0.1914360 10.2567480 5.8785120 0.1914360 8.7603120 7.9381800 4.3107840 6.9282000 9.5358480 0.0000000 2.4212880 9.9978600 8.4301200 0.0000000 11.7869640 4.5022200 -2.4212880 9.9978600 8.4301200 -2.4212880 9.9978600 8.4301200 0.0000000 11.7869640 4.5022200 2.4212880 9.9978600 8.4301200 0.0000000 7.2847440 11.7869640 -2.4212880 9.9978600 8.4301200 -4.8425760 6.6652320 10.9760160 -4.8425760 6.6652320 10.9760160 -2.4212880 9.9978600 8.4301200 0.0000000 7.2847440 11.7869640 -2.4212880 3.3326160 13.5219120 -4.8425760 6.6652320 10.9760160 -6.9282000 2.2511040 11.7869640 -6.9282000 2.2511040 11.7869640 -4.8425760 6.6652320 10.9760160 -2.4212880 3.3326160 13.5219120 -3.9177240 -1.2729480 13.5219120 -7.8354600 -2.5458960 10.9760160 -4.2818640 -5.8934760 11.7869640 -4.2818640 -5.8934760 11.7869640 -7.8354600 -2.5458960 10.9760160 -3.9177240 -1.2729480 13.5219120 -3.9177240 -1.2729480 13.5219120 -6.9282000 2.2511040 11.7869640 -7.8354600 -2.5458960 10.9760160 -7.8354600 -2.5458960 10.9760160 -6.9282000 2.2511040 11.7869640 -3.9177240 -1.2729480 13.5219120 -4.2818640 -5.8934760 11.7869640 -7.8354600 -6.6652320 8.4301200 -3.9177240 -9.5116320 8.4301200 -3.9177240 -9.5116320 8.4301200 -7.8354600 -6.6652320 8.4301200 -4.2818640 -5.8934760 11.7869640 -0.0000000 -8.2386840 10.9760160 0.0000000 -10.7331240 7.6176720 -3.9177240 -9.5116320 8.4301200 -3.9177240 -9.5116320 8.4301200 0.0000000 -10.7331240 7.6176720 -0.0000000 -8.2386840 10.9760160 3.9177240 -9.5116320 8.4301200 2.4212880 -11.5713000 4.3107840 0.0000000 -10.7331240 7.6176720 0.0000000 -10.7331240 7.6176720 2.4212880 -11.5713000 4.3107840 3.9177240 -9.5116320 8.4301200 6.9282000 -9.5358480 4.5022200 2.4212880 -11.5713000 4.3107840 4.8425760 -10.7845800 0.1914360 4.8425760 -10.7845800 0.1914360 2.4212880 -11.5713000 4.3107840 6.9282000 -9.5358480 4.5022200 6.9282000 -9.5358480 4.5022200 4.8425760 -10.7845800 0.1914360 8.7603120 -7.9381800 0.1914360 8.7603120 -7.9381800 0.1914360 4.8425760 -10.7845800 0.1914360 6.9282000 -9.5358480 4.5022200 2.4212880 9.9978600 8.4301200 4.8425760 10.7845800 4.3107840 0.0000000 11.7869640 4.5022200 0.0000000 11.7869640 4.5022200 4.8425760 10.7845800 4.3107840 2.4212880 9.9978600 8.4301200 8.7603120 7.9381800 4.3107840 6.9282000 9.5358480 0.0000000 4.8425760 10.7845800 4.3107840 4.8425760 10.7845800 4.3107840 6.9282000 9.5358480 0.0000000 8.7603120 7.9381800 4.3107840 -2.4212880 9.9978600 8.4301200 0.0000000 11.7869640 4.5022200 -4.8425760 10.7845800 4.3107840 -4.8425760 10.7845800 4.3107840 0.0000000 11.7869640 4.5022200 -2.4212880 9.9978600 8.4301200 -4.8425760 6.6652320 10.9760160 -6.3087720 8.6832840 7.6176720 -2.4212880 9.9978600 8.4301200 -2.4212880 9.9978600 8.4301200 -6.3087720 8.6832840 7.6176720 -4.8425760 6.6652320 10.9760160 -4.8425760 6.6652320 10.9760160 -8.7603120 5.3922960 8.4301200 -6.9282000 2.2511040 11.7869640 -6.9282000 2.2511040 11.7869640 -8.7603120 5.3922960 8.4301200 -4.8425760 6.6652320 10.9760160 -4.2818640 -5.8934760 11.7869640 -7.8354600 -2.5458960 10.9760160 -7.8354600 -6.6652320 8.4301200 -7.8354600 -6.6652320 8.4301200 -7.8354600 -2.5458960 10.9760160 -4.2818640 -5.8934760 11.7869640 -6.9282000 2.2511040 11.7869640 -10.2567480 0.7867200 8.4301200 -7.8354600 -2.5458960 10.9760160 -7.8354600 -2.5458960 10.9760160 -10.2567480 0.7867200 8.4301200 -6.9282000 2.2511040 11.7869640 -7.8354600 -6.6652320 8.4301200 -6.9282000 -9.5358480 4.5022200 -3.9177240 -9.5116320 8.4301200 -3.9177240 -9.5116320 8.4301200 -6.9282000 -9.5358480 4.5022200 -7.8354600 -6.6652320 8.4301200 -3.9177240 -9.5116320 8.4301200 0.0000000 -10.7331240 7.6176720 -2.4212880 -11.5713000 4.3107840 -2.4212880 -11.5713000 4.3107840 0.0000000 -10.7331240 7.6176720 -3.9177240 -9.5116320 8.4301200 0.0000000 -10.7331240 7.6176720 2.4212880 -11.5713000 4.3107840 -2.4212880 -11.5713000 4.3107840 -2.4212880 -11.5713000 4.3107840 2.4212880 -11.5713000 4.3107840 0.0000000 -10.7331240 7.6176720 2.4212880 -11.5713000 4.3107840 -0.0000000 -11.7869640 0.0000000 4.8425760 -10.7845800 0.1914360 4.8425760 -10.7845800 0.1914360 -0.0000000 -11.7869640 0.0000000 2.4212880 -11.5713000 4.3107840 0.0000000 11.7869640 4.5022200 4.8425760 10.7845800 4.3107840 2.4212880 11.5713000 0.1914360 2.4212880 11.5713000 0.1914360 4.8425760 10.7845800 4.3107840 0.0000000 11.7869640 4.5022200 4.8425760 10.7845800 4.3107840 6.9282000 9.5358480 0.0000000 2.4212880 11.5713000 0.1914360 2.4212880 11.5713000 0.1914360 6.9282000 9.5358480 0.0000000 4.8425760 10.7845800 4.3107840 0.0000000 11.7869640 4.5022200 -2.4212880 11.5713000 0.1914360 -4.8425760 10.7845800 4.3107840 -4.8425760 10.7845800 4.3107840 -2.4212880 11.5713000 0.1914360 0.0000000 11.7869640 4.5022200 -2.4212880 9.9978600 8.4301200 -6.3087720 8.6832840 7.6176720 -4.8425760 10.7845800 4.3107840 -4.8425760 10.7845800 4.3107840 -6.3087720 8.6832840 7.6176720 -2.4212880 9.9978600 8.4301200 -4.8425760 6.6652320 10.9760160 -8.7603120 5.3922960 8.4301200 -6.3087720 8.6832840 7.6176720 -6.3087720 8.6832840 7.6176720 -8.7603120 5.3922960 8.4301200 -4.8425760 6.6652320 10.9760160 -8.7603120 5.3922960 8.4301200 -10.2567480 0.7867200 8.4301200 -6.9282000 2.2511040 11.7869640 -6.9282000 2.2511040 11.7869640 -10.2567480 0.7867200 8.4301200 -8.7603120 5.3922960 8.4301200 -7.8354600 -2.5458960 10.9760160 -7.8354600 -6.6652320 8.4301200 -10.2078120 -3.3167160 7.6176720 -10.2078120 -3.3167160 7.6176720 -7.8354600 -6.6652320 8.4301200 -7.8354600 -2.5458960 10.9760160 -10.2567480 0.7867200 8.4301200 -7.8354600 -2.5458960 10.9760160 -10.2078120 -3.3167160 7.6176720 -10.2078120 -3.3167160 7.6176720 -7.8354600 -2.5458960 10.9760160 -10.2567480 0.7867200 8.4301200 -10.2567480 -5.8785120 4.3107840 -6.9282000 -9.5358480 4.5022200 -7.8354600 -6.6652320 8.4301200 -7.8354600 -6.6652320 8.4301200 -6.9282000 -9.5358480 4.5022200 -10.2567480 -5.8785120 4.3107840 -3.9177240 -9.5116320 8.4301200 -6.9282000 -9.5358480 4.5022200 -2.4212880 -11.5713000 4.3107840 -2.4212880 -11.5713000 4.3107840 -6.9282000 -9.5358480 4.5022200 -3.9177240 -9.5116320 8.4301200 -2.4212880 -11.5713000 4.3107840 -0.0000000 -11.7869640 0.0000000 2.4212880 -11.5713000 4.3107840 2.4212880 -11.5713000 4.3107840 -0.0000000 -11.7869640 0.0000000 -2.4212880 -11.5713000 4.3107840 0.0000000 11.7869640 4.5022200 2.4212880 11.5713000 0.1914360 -2.4212880 11.5713000 0.1914360 -2.4212880 11.5713000 0.1914360 2.4212880 11.5713000 0.1914360 0.0000000 11.7869640 4.5022200 -4.8425760 10.7845800 4.3107840 -2.4212880 11.5713000 0.1914360 -6.9282000 9.5358480 0.0000000 -6.9282000 9.5358480 0.0000000 -2.4212880 11.5713000 0.1914360 -4.8425760 10.7845800 4.3107840 -6.3087720 8.6832840 7.6176720 -8.7603120 7.9381800 4.3107840 -4.8425760 10.7845800 4.3107840 -4.8425760 10.7845800 4.3107840 -8.7603120 7.9381800 4.3107840 -6.3087720 8.6832840 7.6176720 -6.3087720 8.6832840 7.6176720 -8.7603120 5.3922960 8.4301200 -8.7603120 7.9381800 4.3107840 -8.7603120 7.9381800 4.3107840 -8.7603120 5.3922960 8.4301200 -6.3087720 8.6832840 7.6176720 -8.7603120 5.3922960 8.4301200 -11.2100640 3.6423720 4.5022200 -10.2567480 0.7867200 8.4301200 -10.2567480 0.7867200 8.4301200 -11.2100640 3.6423720 4.5022200 -8.7603120 5.3922960 8.4301200 -10.2078120 -3.3167160 7.6176720 -7.8354600 -6.6652320 8.4301200 -10.2567480 -5.8785120 4.3107840 -10.2567480 -5.8785120 4.3107840 -7.8354600 -6.6652320 8.4301200 -10.2078120 -3.3167160 7.6176720 -10.2567480 0.7867200 8.4301200 -10.2078120 -3.3167160 7.6176720 -11.7531840 -1.2729480 4.3107840 -11.7531840 -1.2729480 4.3107840 -10.2078120 -3.3167160 7.6176720 -10.2567480 0.7867200 8.4301200 -10.2567480 -5.8785120 4.3107840 -8.7603120 -7.9381800 0.1914360 -6.9282000 -9.5358480 4.5022200 -6.9282000 -9.5358480 4.5022200 -8.7603120 -7.9381800 0.1914360 -10.2567480 -5.8785120 4.3107840 -6.9282000 -9.5358480 4.5022200 -4.8425760 -10.7845800 0.1914360 -2.4212880 -11.5713000 4.3107840 -2.4212880 -11.5713000 4.3107840 -4.8425760 -10.7845800 0.1914360 -6.9282000 -9.5358480 4.5022200 -2.4212880 -11.5713000 4.3107840 -4.8425760 -10.7845800 0.1914360 -0.0000000 -11.7869640 0.0000000 -0.0000000 -11.7869640 0.0000000 -4.8425760 -10.7845800 0.1914360 -2.4212880 -11.5713000 4.3107840 -4.8425760 10.7845800 4.3107840 -6.9282000 9.5358480 0.0000000 -8.7603120 7.9381800 4.3107840 -8.7603120 7.9381800 4.3107840 -6.9282000 9.5358480 0.0000000 -4.8425760 10.7845800 4.3107840 -8.7603120 7.9381800 4.3107840 -11.2100640 3.6423720 4.5022200 -8.7603120 5.3922960 8.4301200 -8.7603120 5.3922960 8.4301200 -11.2100640 3.6423720 4.5022200 -8.7603120 7.9381800 4.3107840 -11.2100640 3.6423720 4.5022200 -11.7531840 -1.2729480 4.3107840 -10.2567480 0.7867200 8.4301200 -10.2567480 0.7867200 8.4301200 -11.7531840 -1.2729480 4.3107840 -11.2100640 3.6423720 4.5022200 -11.7531840 -1.2729480 4.3107840 -10.2078120 -3.3167160 7.6176720 -10.2567480 -5.8785120 4.3107840 -10.2567480 -5.8785120 4.3107840 -10.2078120 -3.3167160 7.6176720 -11.7531840 -1.2729480 4.3107840 -11.2100640 -3.6423720 0.0000000 -8.7603120 -7.9381800 0.1914360 -10.2567480 -5.8785120 4.3107840 -10.2567480 -5.8785120 4.3107840 -8.7603120 -7.9381800 0.1914360 -11.2100640 -3.6423720 0.0000000 -6.9282000 -9.5358480 4.5022200 -8.7603120 -7.9381800 0.1914360 -4.8425760 -10.7845800 0.1914360 -4.8425760 -10.7845800 0.1914360 -8.7603120 -7.9381800 0.1914360 -6.9282000 -9.5358480 4.5022200 -6.9282000 9.5358480 0.0000000 -10.2567480 5.8785120 0.1914360 -8.7603120 7.9381800 4.3107840 -8.7603120 7.9381800 4.3107840 -10.2567480 5.8785120 0.1914360 -6.9282000 9.5358480 0.0000000 -8.7603120 7.9381800 4.3107840 -10.2567480 5.8785120 0.1914360 -11.2100640 3.6423720 4.5022200 -11.2100640 3.6423720 4.5022200 -10.2567480 5.8785120 0.1914360 -8.7603120 7.9381800 4.3107840 -11.2100640 3.6423720 4.5022200 -11.7531840 1.2729480 0.1914360 -11.7531840 -1.2729480 4.3107840 -11.7531840 -1.2729480 4.3107840 -11.7531840 1.2729480 0.1914360 -11.2100640 3.6423720 4.5022200 -11.7531840 -1.2729480 4.3107840 -11.2100640 -3.6423720 0.0000000 -10.2567480 -5.8785120 4.3107840 -10.2567480 -5.8785120 4.3107840 -11.2100640 -3.6423720 0.0000000 -11.7531840 -1.2729480 4.3107840 -10.2567480 5.8785120 0.1914360 -11.7531840 1.2729480 0.1914360 -11.2100640 3.6423720 4.5022200 -11.2100640 3.6423720 4.5022200 -11.7531840 1.2729480 0.1914360 -10.2567480 5.8785120 0.1914360 -11.7531840 1.2729480 0.1914360 -11.2100640 -3.6423720 0.0000000 -11.7531840 -1.2729480 4.3107840 -11.7531840 -1.2729480 4.3107840 -11.2100640 -3.6423720 0.0000000 -11.7531840 1.2729480 0.1914360'
coords_string = coords_string.strip('\n ').replace('\n', ' ').replace('  ', ' ')
coords = array([float(s) for s in coords_string.split(' ')])

# filter doubled values
coords.shape = (-1, 3, 3)
coords = coords[::2,:,:]

coords = coords.ravel()
coords.shape = (-1, 3)

vertices = coords.copy()
vertices.shape = (-1, 3, 3)

# calc center poins
middle = coords.copy()
middle.shape = (-1, 3, 3)
middle = middle.sum(1)
middle /= 3.

leds = [
# row 1
[92, 91, 98, 90, 97, 102, 104, 101, 103, 100, 99, 93, 84, 74,  83,  72,  73,  62, 50, 36, 45, 31, 44,  32,  46,  47,  60,  59, 71, 82],
# row 2
[70, 69, 81,  68,  80,  88,  96,  89, 95, 87, 94, 86, 85,  75,  63,  51,  61,  48, 49, 35, 23, 13, 19,  10,  20,  21,  33,  30, 43, 58],
# row 3
[42, 57, 41, 56, 66, 78, 79, 67, 77, 65, 76, 64, 52, 37, 24, 34, 22, 12, 5, 1, 4, 11, 9, 18, 29],
# row 4 
[17, 28, 39, 54, 55, 40, 53, 38, 25, 14, 6, 2, 0, 3, 8],
# row 5
[15, 26, 27, 16, 7, ],
]

# concatenate all rows
all_leds = functools.reduce(lambda a,b: a+b, leds)

middle_sorted = middle.take(all_leds, 0)


def plot_model():
	X = coords[:,0]
	Y = coords[:,1]
	Z = coords[:,2]

	from pylab import figure, show
	from mpl_toolkits.mplot3d import Axes3D, art3d
	import matplotlib.colors as colors
	import numpy as np

	fig = figure()

	def plot_array(coords, style='.'):
		X = coords[:,0]
		Y = coords[:,1]
		Z = coords[:,2]
		ax.plot(X, Y, Z, style, picker=5)
		fig.canvas.draw()		

	def plot_point(coords, id, style='.'):
		plot_array(coords[id:id+1], style)

	def plot_row(row, style):
		for led in leds[row]:
			plot_point(middle, led, style)

	def onpick(event):
		ind = event.ind
		print(ind[0])

	fig.canvas.mpl_connect('pick_event', onpick)

	ax = Axes3D(fig)

	tri = art3d.Poly3DCollection(vertices)
	tri.set_color(colors.rgb2hex((1, 1, 1)))
	tri.set_edgecolor('k')
	ax.add_collection3d(tri)

	leds = middle_sorted.copy()

	plot_array(leds, 'yo')
	# plot_array(rotated, 'ro')
	# plot_point(coords, 53, 'bo')
	# plot_row(0, 'yo')

	show()


if __name__ == '__main__':
	pass
#	plot_model()
	