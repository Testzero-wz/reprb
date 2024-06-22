import warnings
import random
import string
import os
from reprb import reprb, evalb, dump, load_iter, load

warnings.filterwarnings("ignore", category=DeprecationWarning)


def random_bytes(size: int) -> bytes:
    return bytes.fromhex("".join(random.choices(string.hexdigits, k=size * 2)))


def test():
    print("Test:")
    testcases = [
        b"123",
        b"True",
        b'"',
        b"\\'",
        "abc\x00\x01\x02中文\t\n\r&*（￥%%……&%*".encode(),
        b"'\"\\",
    ]
    pass_cnt = 0
    for t in testcases:
        r = reprb(t)
        e = evalb(r)
        if t != e:
            print("Error: %r != %r" % (t, e))
        else:
            pass_cnt += 1
    print(f"({pass_cnt}/{len(testcases)}) Testcases passed. ")

    # test dump/load
    dump_bytes = [random_bytes(random.randint(1000, 3000)) for _ in range(1000)]
    tmp_dump_file = "./.tmp.dump"
    with open(tmp_dump_file, "wb") as f:
        dump(dump_bytes, f)
    load_bytes_from_path = load(tmp_dump_file)
    with open(tmp_dump_file, "rb") as f:
        load_bytes_from_file = load(f)
    load_bytes_from_iter = list(load_iter(tmp_dump_file))

    # remove test file
    if os.path.exists(tmp_dump_file):
        os.remove(tmp_dump_file)

    assert (
        dump_bytes
        == load_bytes_from_path
        == load_bytes_from_file
        == load_bytes_from_iter
    )
    print("dump/load test passed.")


def benchmark():
    def bench(func_desc, func, input, bench_times):
        total_run_time = timeit.Timer(lambda: func(input)).timeit(bench_times)
        # bytes per second
        bps = len(input) * bench_times / total_run_time
        print(f"{func_desc}: %.10fs, %.2f bytes/s" % (total_run_time, bps))

    import timeit

    bytes_msg = bytes.fromhex(
        "16030108b1010008ad0303b34832156a2c27f12f8450fd4e94b306015b09e2fdc430b4fffb3fcc056a080920471b1572c095540d932c93510337d3adf531b1c619d96948b4686ae6b7b1146e00201a1a130113021303c02bc02fc02cc030cca9cca8c013c014009c009d002f0035010008447a7a0000ff01000100001b0003020002003304ef04ed6a6a000100639904c01c1a3c7905f15baf081999c4a83db0e614b7d6886a792c0718f7a28ac6c07833c11652b52c95cfeac20ab48f5f2b74bbf584aa35b9801687322928118229f0ab2a2e7105106a86b7bbb3e0b73b62a05e182ab4f42c0fdb117481582efdc9ccec173f8aec34e06a0c93615859e0244458bd93653f26baa04419752376cc7a205d48d4a4284c547471770d03809ee3c67f8c40adc2b34c68a912399b3aeac5e879b2d1c80426e9cb7c4cc4e757cd5703c307a8867758ca3e31b98dac9c29f18039ac6f2cccc1f97aa46f39786a1196d86b41dca960a075203203044c838bbef20bdb9390a0083561985daeba7246d222826a5942c9c231275728dc3923cb2a718a373a324641a20cb874c2a3922753f87cce32a96d883477f59b1f2b70d997ab36874ed0f03527e265da32a58b6a9b43ea21b67c2623e23cc5136967d83e09611b580286a8737e30f35762fb0597b97f3d548e94843972d1886b94adcb99b062f205b053a01ec500a61c3ef19228328395b6ac2ce2365a0f439ae7300df9e14368da3412e9b519e4844fd5c2e57b7627383dd269a28abc9d25f283eb39c450f08198c843f5202aa1cbcf2b925bcc51222ae893915727ffeb55e6043d2a7383a3d439c86583fbda712ed6aa48675afac53fb2e6633d9796c0755ab2011670ea165d1b563c0b1430f96ac212bad9a81d53c442734070844b0d2851a4126b3632b10a2c6a058eb59156c2be01e8beaa760211b735b0e99f45f0685df31ac41a704034ba4556976a990bf5ab3129862c16946197d942de5c6b4253be5aac7f1a507849c02c07c67b08566d0e5cb91714164f658e92882978021b0ae66d677c0b4a99535f454358fcb1866c3d9dcb0e46c968dc59a8ab93099e1327a05c70a1830aec4b9842fc4849f68f5b9083817cc334159af86978bd9192b307547a9bb9d7f135c8b0a51bacb6f2f59453f82766f9149f2273d1b85aaee870e82086150ccedccb4d08133fee01746eab3d0bca49d42c3a66403d6e0736491a9798940325c5a4bb6c6b0eb2074394498367a287e9711a3966f1a036b8fa8a3fabb498ac25bb318b14c9159344bab698cac42c1ba9f3554be0b763a37b7eb15ebceca248c03c290145415514d6e49018dc74dfc1a82d665d121520ede05f945c2ed5ec36cb41ca59b256f95168723c9116a27aed52a09c1481d6a09dc8c08d07e978187b39478cb8d1915e2d56187a996313a35df308742ecb7e187497f1c551370130c3f711f7e57b1ef027dc3682672787a0e05557115ff69340c1661c4460880f67a0618a045b1065e8a891525693da3a05910303797c6cdafb3fe69844a5a0bd82e11a12e84f715352457b3d32dcc7bd6a3489a11cf4bb7f4dec82df60640cb6b9d422909c0438db2ab6d694123c25b0f6c76767797966a945458cc256abbebc3571e6e9014d4041baf56b1604716f4260d5e37cc8b17ad63599f1c8c7c9771eced70d25a91a4cfb699b1949c122a0879121e9b716f83097df202b59e6cb174a7e318072d42584f6c4646a618093b316df1916d90b2840a43fe35600df1956e694aa9db56870a469a711a8e086731bccc80d47496528c699049d733a75dee28164252fe426426300ccaefaa298f4a58ac21cc0a6064cc60830323638590080c62493034af13508df157ec15415cfde02a16df656be6f629d858ca10ef49e6d3ab2574ec28e5a3a001d002011e3d4c98e160a18b9ca506668754fa60b13be8965d72a80646402bd97019c480010000e000c02683208687474702f312e31000d001200100403080404010503080505010806060100120000000a000c000a6a6a6399001d00170018002300000005000501000000000000001d001b0000187777772e676f6f676c652d616e616c79746963732e636f6d00170000002d00020101002b0007064a4a03040303000b00020100fe0d00da000001000156002021350f48311c29c6ac800d04d7b6f46a87935ce6110e6b0ac66b444c39c7f17300b0ada364a112c59421c24c31e8caf7c398b09a6517a65ac1fbc53e9a209cc6990053ce8b5236244385fa0a980a929c48a59f2975a22c58048b21bbbbad2bc6d3894d9167c02ef2baec4b1c0230847607cb97a3361c75abc9f00880df0830c21878a7259e863e6f69167eacb104abe306a92b920b712a8ec16ea4bfa510b3fb56b6a5bad4767966dac3d3b0d239531712d5f72aa2d6610d6e737bf3f386c6bc5823bcb231efa37a432c8b482d070eae09a44469000500030268325a5a000100002901cc01a701a102fe26bd498081e8fa0a6587e9fe2c03fcf24d3f8ca56460a0ff7d70e9da9c6572d333bbce3a6c0d5b5c87e25b6ba26468c1a235cf04ad6700fae4c8b3acc5d14099949f015290afec635affdf099925de226046ec4c2e3675a1236661300c5537a4a444b7ccf8d05963b4cebc84f0424351b9b62f26f1ae9f1e78e9f51682006de197db5c6af6cb583e60918bc2216270eb14f9858294636f0f9d5bd0d5ef613d6d0dd88ab1067d5b9574d2a51b6c3d2377e0ba340677af0de09fdf96c6e422dd36dcc6abd3ab421542a241b491af011c36072ec974e1a66560178648b5186efa4f77fce358df9180adcd108beffc2608a0ceb06b602e44a6fea1941bbe804599e3c208fd24bf182e40af73adbca5bac3a0a4b6bb0c679c161b751ac19ed02ac110c091feec24b10d05273595f50d29d3537943b8e7e88e2fb95e4a0b65b57f4f46bf599d2845369b16abd1f023e0fed423a7851fd53706c3e366fb3c2a0372193877eecc136ca384ec788ea1ec13fe93f7dd0a2056f8c104efb2978d5409891e53ac85825bf1258a6e069a408c9b283fd5ae67fb6853494e2a0250865bdaf7f08e99d34a002120a49333eacdc6464e941a8db3537f3fe3035c8e7fd6d5678b84a57e548e7de027"
    )
    reprb_bytes_msg = reprb(bytes_msg)
    repr_bytes_msg = repr(bytes_msg)
    bench_times = 100000
    print("Bench:")
    bench("built-in repr", repr, bytes_msg, bench_times)
    bench("built-in eval", eval, repr_bytes_msg, bench_times)
    bench("reprb/dumpb", reprb, bytes_msg, bench_times)
    bench("evalb/loadb", evalb, reprb_bytes_msg, bench_times)


if __name__ == "__main__":
    test()
    benchmark()