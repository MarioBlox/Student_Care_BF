import httpx
import json
import re

COOKIE = "PHPSESSID=nanqj8v0vl5amuna2q58alj002; LAST_LOGIN_USER_ID_SDC=153590; auth-save=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJJTlNUSVRVVEVfSUQiOiI5MjYyIiwiSU5TVElUVVRFX0xPR0lOIjoiMTA3MTAyMDQ2MyIsIkZVTExfTkFNRV9USCI6IiBcdTBlNDJcdTBlMjNcdTBlMDdcdTBlNDBcdTBlMjNcdTBlMzVcdTBlMjJcdTBlMTlcdTBlMjdcdTBlMzRcdTBlMmFcdTBlMzhcdTBlMTdcdTBlMThcdTBlMjNcdTBlMzFcdTBlMDdcdTBlMjlcdTBlMzUgXHUwZTA4XHUwZTMxXHUwZTA3XHUwZTJiXHUwZTI3XHUwZTMxXHUwZTE0XHUwZTAxXHUwZTMyXHUwZTBkXHUwZTA4XHUwZTE5XHUwZTFhXHUwZTM4XHUwZTIzXHUwZTM1IiwiU0hPUlRfTkFNRV9USCI6Ilx1MGUyNy5cdTBlMmEuIiwiRlVMTF9OQU1FX0VOIjoiVmlzdXR0aGFyYW5nc2kgS2FuY2hhbmFidXJpIFNjaG9vbCIsIlNIT1JUX05BTUVfRU4iOiJ2LnMuIiwiQUdFTkNZIjoiMTAxIiwiTE9HT19JTUciOiI0ODJiYzFjNi01MDNhLTQwYjQtOWQyNS1kYWE2YzEyMzYxOGUucG5nIiwiQkFOTkVSX0lNRyI6IjhhZWNjNzhhLTlkZGQtNDI3MS1hM2Y5LWI2NmQyYTI3MWExOC5wbmciLCJTVEFUVVMiOiIxIiwiTE9HSU4iOiJhZG1pbiIsIlBXRCI6ImFkbWluc2MiLCJMT0dJTl9JRCI6IlZpc3V0dGhhcmFuZ3NpIiwiU01TX1NUQVRVUyI6IjAiLCJBTExPV19TTVMiOiIyMCIsIklOU19JRCI6IjkyNjIiLCJSRUFMVElNRV9TRU5EX1RZUEUiOiIxIiwiQ0FSRF9UWVBFIjoiMSIsIlRFQUNIRVJfRk5BTUUiOiJcdTBlMjhcdTBlMzRcdTBlMjdcdTBlMjNcdTBlMzFcdTBlMTVcdTBlMTlcdTBlNGMiLCJURUFDSEVSX0xOQU1FIjoiXHUwZTFlXHUwZTMyXHUwZTIyXHUwZTM4XHUwZTJiXHUwZTMwIiwiVEVBQ0hFUl9OQU1FIjoiXHUwZTE5XHUwZTMyXHUwZTIyXHUwZTI4XHUwZTM0XHUwZTI3XHUwZTIzXHUwZTMxXHUwZTE1XHUwZTE5XHUwZTRjIFx1MGUxZVx1MGUzMlx1MGUyMlx1MGUzOFx1MGUyYlx1MGUzMCIsIlRFQUNIRVJfSUQiOiIyMzk4NzIiLCJJTlNfVVNFUl9JRCI6IjI0ODgwNyIsIklOU19VU0VSX0xPR0lOIjoic2lwYXl1aGFAdmlzdXQuYWMudGgiLCJST0xFX0lEIjoiMzA2MjMiLCJVU0VSX1RZUEUiOiJ0YyIsIlVTRVJfTE9HSU5fSUQiOiIyMzk4NzIiLCJMQU5HVUFHRSI6InRoIiwibGFuZ3VhZ2UiOiJ0aGFpIn0.cJd32lxPuYuE-N_lsSz3ZUak4jwmDcpV0NE1TLD6Wgs; ci_session=Qw5vURZXBLMswn4a3VuI9Z%2FdbpWdJUOaBBYDu%2ByDgygnBGDUxUGLVA5JGDWaLG0IY0kbSxEAU87e1iA2LGdZPaf4PR2ovnxJ%2FaNpcwwMhYENMbjXq9iuMyONH9JTdP9%2F0LcPSfWfym3uJ1yNsk5yT9spg1%2BYxeh0WudYqny8vuapTPeahmTetoYziBX1dj55VVQd9JyMXhEuvLWjFmh68jDKmPR0u%2BK4N3uhGZk0l%2BFILQW4aPBWC%2BDJ%2Fzn3EAfXIFw1%2BXqXMdgxF2NeEbvqO2A7NUBCfL%2Fy6f92jgxkxHh3I2EcTIJlY5C8hzyCgSrgdW1n0MiV260l79HthIPcG0KJW1EfLzuGjgSo5z7wHfgEcoDhZyEuhA4%2FOt9d7fG1V%2BpwXp0977lV5ffi5YhZpq1fsIcalM9E5xeSOwCAYbCnCSG4%2FQub63kwy7BcZMIdP40a1UNfje76VfxeITf4v9OMa3nAFm%2FZd%2B3BdPhBGtxrsEhGJnQ%2BZtQdYIal%2Baa089GQc%2F1oSnRGMPmCU%2B8h8wQLOPFJKSliTW7KA5GUqUIU7n5yAT7v6tPGmGpT3Pj%2B0FfANFfpyvYlUwEga5zdWFC8aLaJxmjkqR%2BGOZRAy7%2BoE6QXDdkMigQz0lk0Hzc0Wdf79aApRJBlbQTaNSF0yrqX5Bm92gl8RexliJxnmDGTvLskr51spI%2Fukq%2BsAAWZ5bPAVd2qWwB8SHgmi7XfXyHjf%2BeH09cug5zj842vH%2BfUU1zgcyTcaElsScQxGgx7bZeY9kLYh6PFKtCnjD8i55ZwYeyLUpzTIg%2Bu%2BYkLL7kqi%2Bl06AE%2FDsj9qthGyZlicm0IoeMQr%2FDcds8vQUiJGihzdw7jsNkjyknjuyvBoYRJlakW%2BFxTCHtY2rAP%2Fh6OMsJR%2B2onQz9PukuIuNXMg0%2F5g0mAlCh00TuRTiAkWCicJn1UtskaAaE%2B80yHwKFwpE8XXx1lzsvx6K9gpcVZRSK28J184xoMAbzF2YUB0wt%2B0WAEJ97II3bsZLC%2BCg9RYOkdl%2Ba76zpWQLlq5%2BpHs6U%2F4SgJCi5GJENdscV1GSoVv2j3BULLQ4bjXh3nBpE18C%2Bc3YDwNqOQC85AdckElWOoT%2FxDNf3W%2BieTAr1pkufIX9I9EEg103XoGcFvHpGfFe%2FkVILRGnUIp%2FIkrfaGjrk0j5iF%2BzxGjARmY2U618L9vLPtOI5VJu7P5z2ywThf59f27yDntlM64Fkssa%2BhOGmHX0NARFFZxEPkmz21ACTYFtqKSh%2BVoFF2cZWgM8jvj6pgLISX%2BtQ5P3Kr7ZkQpaUINqT6gv8Z6Dt8b5CzvRK7c19D7lGDjDBrcYzm3HBbHj%2Bm%2FLlAUtCYfrB%2BKeI1xQDaR1c85M8QdK7hip%2BMzhIhCzyO%2BBYJ0xGid%2FpjOEwHwjr2JDRFG67%2B3X%2BDnSdKyGcLsa1KIHMHDMUB5RZGwtdzLaibiWW3kug1TGj1DJ1BS1ZHBSUMKohzyqu5%2BFZ3A0NdSxCMfJ9VirGzd1ePt0PKhcmjDXUev%2Brb1pmC2%2Fn260%2BuFFCocF%2Fen%2FBRS3afVJKfcbiFMai1dsR2j10l2Hy8JhliD2i%2FJjGhj60kmw7zvJ0u9djwEZOwR6LhE%2FwFaWNwzZnwkYCl5ST1vqphZdi1JYnyLY0IuA2y7tqE%2FgSYXfOzIqeP92XUzGwTsJTwnQ8d8EAz6QdByVZvut0Gw6%2FpRvtuPE67465lBS%2BjWClbq%2BGyKFWLu92Y%2Bv5qtZ6uzCgW3uZ%2FtG9L5ZYU9G%2Fd9u2S8%2Bf0xXk4eRfj%2F5ZMgadDdShkB305N266WvmqVoBIuhU4ItVk36GAQtaX9V%2FPOWwi6O%2F33vPltcbVQ%2FmYrKhH8zBFh18FBV6mN8ItJDBEv5M7bAEKaDExPeuFOf23IUlSP3HCRzer7ZDCoDeYPQfWQ472yxH5EudQUA%2FACAB1OJo0u1%2BpedeEtRRS5wF5fSpYYsE3TRBECZe8spm9pTXU%2BB36lxb1ayX%2FAyNPxtajQ3%2BgibnOa2UWSBoQl5GEGus7lkW0KVZmQMJDeKm2DxcHd0JXmDlxUdPpcSVN%2FHl2E19%2F0Gkjs%2FVTVV1Jea2BbpyYrc9z%2Fzf2BUR3n0OfEkw0R%2BJVaV4hWcqsVB8BqHb8ixH%2FAUQ0Ah4eRkUCbTkXHV1RjTHEKx9O2OHUQq3fBTK5hsc7kJlFskTNtkl2o3e5gfOTODZhLDYFP7mPlAZbeSZWhMQMJXsQ9DFWumnIzwv4QsQXQRHszkmxC7G4pUUfdc1YL0DQ%2F%2BX2JEvJiEpuEGWAQEV0A0QLYCeop5UFNcCFrAgz1z8piHQ0mB8T21u1Hmx0KaSXj6DRB2SwlNUp6%2BRnLCzAR79OjyyMHTFu64VAYMaFhcSlxVX2C%2FOXCyKW94kk%2Fe2rjJbzcLpVvDM%2BViysB813nEkPKpO6vNFVBW6FiFwYPL6H9eY46zDITASXFORqsAbFOTPin1yQP2YjWCNCPu0LVl1s5sHyjaQju1QWBkEpqPLjWZGqDHB9UuK5oyu9nLdNbj58L3FrJ07XfgEMxguGHa6M6uPitmg9Ft04Gvd1kwyFyap2FVKjThsuPwGR%2Fyz4FniJgVvz4%2BYYykO%2BSqpFJ2JBqXsMNRg7hLYp8dwRjNQ%2FBxtxBsknO7%2FZbQ%3D%3D"

headers_common = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "cookie": "PHPSESSID=nanqj8v0vl5amuna2q58alj002; LAST_LOGIN_USER_ID_SDC=153590; auth-save=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJJTlNUSVRVVEVfSUQiOiI5MjYyIiwiSU5TVElUVVRFX0xPR0lOIjoiMTA3MTAyMDQ2MyIsIkZVTExfTkFNRV9USCI6IiBcdTBlNDJcdTBlMjNcdTBlMDdcdTBlNDBcdTBlMjNcdTBlMzVcdTBlMjJcdTBlMTlcdTBlMjdcdTBlMzRcdTBlMmFcdTBlMzhcdTBlMTdcdTBlMThcdTBlMjNcdTBlMzFcdTBlMDdcdTBlMjlcdTBlMzUgXHUwZTA4XHUwZTMxXHUwZTA3XHUwZTJiXHUwZTI3XHUwZTMxXHUwZTE0XHUwZTAxXHUwZTMyXHUwZTBkXHUwZTA4XHUwZTE5XHUwZTFhXHUwZTM4XHUwZTIzXHUwZTM1IiwiU0hPUlRfTkFNRV9USCI6Ilx1MGUyNy5cdTBlMmEuIiwiRlVMTF9OQU1FX0VOIjoiVmlzdXR0aGFyYW5nc2kgS2FuY2hhbmFidXJpIFNjaG9vbCIsIlNIT1JUX05BTUVfRU4iOiJ2LnMuIiwiQUdFTkNZIjoiMTAxIiwiTE9HT19JTUciOiI0ODJiYzFjNi01MDNhLTQwYjQtOWQyNS1kYWE2YzEyMzYxOGUucG5nIiwiQkFOTkVSX0lNRyI6IjhhZWNjNzhhLTlkZGQtNDI3MS1hM2Y5LWI2NmQyYTI3MWExOC5wbmciLCJTVEFUVVMiOiIxIiwiTE9HSU4iOiJhZG1pbiIsIlBXRCI6ImFkbWluc2MiLCJMT0dJTl9JRCI6IlZpc3V0dGhhcmFuZ3NpIiwiU01TX1NUQVRVUyI6IjAiLCJBTExPV19TTVMiOiIyMCIsIklOU19JRCI6IjkyNjIiLCJSRUFMVElNRV9TRU5EX1RZUEUiOiIxIiwiQ0FSRF9UWVBFIjoiMSIsIlRFQUNIRVJfRk5BTUUiOiJcdTBlMjhcdTBlMzRcdTBlMjdcdTBlMjNcdTBlMzFcdTBlMTVcdTBlMTlcdTBlNGMiLCJURUFDSEVSX0xOQU1FIjoiXHUwZTFlXHUwZTMyXHUwZTIyXHUwZTM4XHUwZTJiXHUwZTMwIiwiVEVBQ0hFUl9OQU1FIjoiXHUwZTE5XHUwZTMyXHUwZTIyXHUwZTI4XHUwZTM0XHUwZTI3XHUwZTIzXHUwZTMxXHUwZTE1XHUwZTE5XHUwZTRjIFx1MGUxZVx1MGUzMlx1MGUyMlx1MGUzOFx1MGUyYlx1MGUzMCIsIlRFQUNIRVJfSUQiOiIyMzk4NzIiLCJJTlNfVVNFUl9JRCI6IjI0ODgwNyIsIklOU19VU0VSX0xPR0lOIjoic2lwYXl1aGFAdmlzdXQuYWMudGgiLCJST0xFX0lEIjoiMzA2MjMiLCJVU0VSX1RZUEUiOiJ0YyIsIlVTRVJfTE9HSU5fSUQiOiIyMzk4NzIiLCJMQU5HVUFHRSI6InRoIiwibGFuZ3VhZ2UiOiJ0aGFpIn0.cJd32lxPuYuE-N_lsSz3ZUak4jwmDcpV0NE1TLD6Wgs; ci_session=SS6Hcj32oLIT4zD2E5%2BC4Uj9c8Dwuy%2BLMiin5FLSZA5zGpeAWPqfWqNXcdltiOS1N4N7flhCNTwAaZ4J2aBNZ8DGjQMO1%2F8dlg%2Fj5q7z5iW8oEE%2FItwyk9fgQX68kDnI4EMhEP885WC1Nq8XJTm7JmTed2ZFzAGtcMN3VPQU9erxXFBZNpTvejxy36bY%2FifYLiw0UbSLy3cZUOAFHhheR%2FnNRrrBeLfohMpFWyywWUY1p8t2Tj4XDjxC6gQuxfhVQ%2BWzFH6wJiaj7hkN1To%2BFV4AN97pKHTZC8Lj%2Fu8g7BT8LKzJ2G%2BwgqF%2FQyAZN037TkgaGo2L97PenNCRRY4vtDonKvlhY69AwyKtJNbhT%2FwpsENHTgw33HBjHrkpBOdGSyDRy5k39K7ZsUrH53Ccre1AMX4nPQh72TmWTaC9iccZPytSnq2%2FHdJBEHPUH7iDg8m7WsdAlbNS49gWKCWlH%2Fz4DCfE%2BC7bcAteFnnnTP4wd1xC0wwTQaC7pF9sCQPZXylCdQphwMxXDDMNt4sfDs5OSf3leIS7B60TiN1FL%2F11oiJbamNb1X0BPH7GBc4CIMLHb2YiZcjrktWnobjpErl5CBRrMGCFG7G66hki%2FDUnva8KlQDDC2tSJH1MbU%2F82rmGgw3WTban2kV36vNYo5y9SboqSfqJWQgU7u96x2Ml9KxBglrON7zGGPj5uA9QTM1NZvygwKwMyoqaK9FkC8321R%2Fx2m%2FsY2SQoux9GSKx69%2BxS5plfbcTLgveYKZAWhZtOslyXLXndTHR%2Fmnu%2B776IRU%2FmQuYw%2BzI%2Ft0eo0LFqyKPzP%2B1AIrK3%2BcPU%2BX1Jg7CTeEy3u%2BK4Ygfexs3qO5kCCnjqL9370FyghCcJWfJbtgn8cvlNfE0XP2emFABY%2Fuyfj8ws6K4LFpqlW7lS6xut%2BFcLwBXGFgHRfmg5itzXPDGVMZ7SKy1TR7SpcEwNqZxjA8hCSd6x0o1sY1wo9vw4ZYUN%2F6E2IVestSxtf2JZM8rjmnGMKBEVrYen2R3ozzzVXE3QwfKOT3BLcSQPkZaeYumb8zqFehnN6UiWJQXd5I0xzI%2FZUjluE9Q1JXxzKhtwE8%2FSTyEzceFc4CjGKrwf2iSzFoS6dh3B2NeddV1lO0TPXqv5Aqy7h2c4ZfM8z9Y2C2g3%2BnZqpHq91rJ%2B4q32auflgf4sgjUY2ZD0NotQo4kc50gqL4JstVof5fotCSiQNu0mTPa259%2FU723zyRDbZK92NWSdVvKuYl1PKXtziJ4xhKk9lIjSZFElWEJgOd0RsY08pe%2F%2BesuJBSVeJZ%2F5l%2FwbsNnR1WkHt789ryaSpAXBvPGUdLfuluDwfToKiggiGUXkP07knGllo%2FaumhgFUJYkmiCZ0zb9euHMMa9CYA9qABykdYzgnKPeyWDs3AnwE2H%2FyvO4C%2BH%2FVRXvTvFOBGSXeBeqnMhs1qgWpcWwBbJpkEwBFkke%2Fccvgml3CGnZCbXmGuVlL5JZU9yJ612jOfTtJn1ltbFK4gg0CAU3eiRrcCGSpQZ0fMYeRvq7g5IGzGQixGKpsfFVsAGCTstbS3RJFCW1jyqZ0wjh37uOJavXViCO14aM0lu9FmvzICkYwm00i5FqP%2F52nUqvao5QftAzwQKRYR2%2FhHuHl%2FpCgfv7wr4O9R%2Fbm67QHzbLWy5gYeksbk28XZ49ohLxi1QBoxMTC0YIz21PsOlHbj71UMbFL3SFQGdz8CaE5DvjOhaFxs1EF61%2BLax4jKvrwqXPA7yqKznd4olBGJXjNGgqPjRXRNwMl0jcY3XNhOqoWjdRLFmYa7uZZirnMJ%2BKlVAgwZjsVIQRhK2SPSuEz9QteLZueXMucG%2FcPY0XFuUL0pVAK1b2lBkUs2JwdoTo9BHK5s2C9xxzQ3p%2BRuj179IEs9%2FV2R3LoDTUYuxs7jsZ12oJtgRCnsGZFob1we%2F7WbiErSPqZzQ7UFECl%2B%2BzW6ELqKTfJp2AiZlazFLdP5NTO1Bk9%2F%2FQ5dLV8GLsjvD6F12a3TZ8UKPh%2Bxb50WP6raQkSGLo2DhJm3zvcm%2BKAre18KUnYgbY619pJFDQR8eU6NGN%2FteVrtkA5KgIAB7%2Fw1DZ%2FrLnEuVX8lZu0AEiNpJJ7gmy16ZQq9MicKqj36BoQPxdi%2Fwb%2FhDqxwUKNQ1hcIglWDllhMotB75jfEf3QeWSrUlWQhhXOYoXjnJmfWvDsKSSVg%2Fn9ORrRU3DOr2IhCMiUpIVC%2F14m0hAshqhtj75j7HozGL4wnDsRALAJeohajO6fNKzB5hXQEXRQMhApmCx4PE%2BzlKCydu9%2BQtsc5IP6QcdSteWq8EXsl8AHEI1umoRPyMG4gtwe%2Befloft7BhumQ6Dgf4pEE6VcfbP52N3Y%2BNA%2Bt2DtOCwRQfASxlXlQiBJv0sl1wf7jLj2Vyw6ZWpINY64%2F4x1x%2BaOEkJABW4gLtZ5y0IS843Vh8MwqhFO5eaQ%2Bq7hkHnutKO%2FubO8sJBKW7O9VBgQJzBhDOjcB8qjSoFLznS5DBsqkIL1NPayH%2FEhRLZ2LoVt1MBgKCpT26o8WYgS%2Fdxersa6D%2B7jHLnrZ5BKJIDk0toARVWNmG3jx1uhMdCqBEHB1pMSFjKhUu4NB2CbS5by31o7ViIyVwC5NX4JZc81INhtcgQaAm5A%3D%3D",
    "Referer": "https://webapp.student.co.th/index.php/school/student",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

def fetch_and_save(url, referer, body, output_filename):
    headers = headers_common.copy()
    headers["Referer"] = referer

    try:
        response = httpx.post(url, headers=headers, data=body, follow_redirects=True)
    except Exception as e:
        print(f"❌ HTTP request failed for {output_filename}: {e}")
        return

    if response.status_code == 200:
        try:
            data = response.json()
            with open(output_filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Success: {output_filename}")
        except Exception as e:
            print(f"❌ JSON decode error in {output_filename}:", e)
            print("🧪 Raw content preview:", response.text[:300])
    else:
        print(f"❌ HTTP {response.status_code} for {output_filename}")
        print("🧪 Raw response preview:", response.text[:300])

def fetch_all_students():
    all_data = []
    page = 1
    per_page = 500
    start = 0

    while True:
        body = student_body.replace("start=0", f"start={start}").replace("page=1", f"page={page}")
        headers = headers_common.copy()
        headers["Referer"] = student_referer

        try:
            r = httpx.post(student_url, headers=headers, data=body, follow_redirects=True)
        except Exception as e:
            print(f"❌ HTTP error on page {page}:", e)
            break

        if r.status_code != 200:
            print(f"❌ HTTP {r.status_code} on page {page}")
            break

        try:
            json_data = r.json()
            rows = json_data.get("rows", [])
            total_pages = json_data.get("pages", 0)

            if not rows:
                print("✅ โหลดครบแล้ว")
                break

            all_data.extend(rows)
            print(f"📥 หน้า {page}: {len(    )} rows (รวม: {len(all_data)})")

            if page >= total_pages:
                print("✅ โหลดครบแล้ว")
                break

            # เพิ่มค่าทีละรอบ
            page += 1
            start += per_page

        except Exception as e:
            print("❌ JSON decode error:", e)
            break

    if all_data:
        with open("student_raw_data.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print("✅ บันทึก student_raw_data.json แล้ว")
    else:
        print("⚠️ ไม่มีข้อมูล student ให้บันทึก")

# ----------- Teacher -----------
teacher_url = "https://webapp.student.co.th/index.php/school/teacher/getAll"
teacher_referer = "https://webapp.student.co.th/index.php/school/teacher"
teacher_body = "keyword=&STATUS=%E0%B8%9B%E0%B8%81%E0%B8%95%E0%B8%B4&POSITION_NAME=&GROUP_ID=&ROLE_ID=&ORDER_BY=1&draw=2&columns%5B0%5D%5Bdata%5D=_checkbox&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=_numrow&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=NAME&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=TEL&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=GROUP&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=EMAIL&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=POSITION_NAME&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=ROLE_NAME&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=STATUS&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=REFERENCE_ID&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=_option&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=false&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=2&order%5B0%5D%5Bdir%5D=asc&start=0&length=300&search%5Bkeyword%5D=&search%5BSTATUS%5D=%E0%B8%9B%E0%B8%81%E0%B8%95%E0%B8%B4&search%5BPOSITION_NAME%5D=&search%5BGROUP_ID%5D=&search%5BROLE_ID%5D=&search%5BORDER_BY%5D=1&rp=300&page=1&orders%5Bcolumn%5D=NAME&orders%5Bdir%5D=asc"

# ----------- Student -----------
student_url = "https://webapp.student.co.th/index.php/school/student/getAll"
student_referer = "https://webapp.student.co.th/index.php/school/student"
student_body = "TERM=28924&LEVEL_ID=&CLASS_ID=&CLASS_GROUP_ID=&PHOTO=&CARD=&keyword=&STUDENT_STATUS=%E0%B8%81%E0%B8%B3%E0%B8%A5%E0%B8%B1%E0%B8%87%E0%B8%A8%E0%B8%B6%E0%B8%81%E0%B8%A9%E0%B8%B2&ORDER_BY=1&draw=3&columns%5B0%5D%5Bdata%5D=_checkbox&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=_numrow&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=student_no&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=std_no&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=name&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=nick_name&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=mobile&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=semester&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=classroom_short_name&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=classroom_group_name&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=false&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=picture_icon&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=false&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=card&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=false&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=parent_name&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true&columns%5B12%5D%5Borderable%5D=false&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=parent_tel&columns%5B13%5D%5Bname%5D=&columns%5B13%5D%5Bsearchable%5D=true&columns%5B13%5D%5Borderable%5D=false&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B14%5D%5Bdata%5D=count_parent&columns%5B14%5D%5Bname%5D=&columns%5B14%5D%5Bsearchable%5D=true&columns%5B14%5D%5Borderable%5D=false&columns%5B14%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B14%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B15%5D%5Bdata%5D=student_status&columns%5B15%5D%5Bname%5D=&columns%5B15%5D%5Bsearchable%5D=true&columns%5B15%5D%5Borderable%5D=false&columns%5B15%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B15%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B16%5D%5Bdata%5D=_option&columns%5B16%5D%5Bname%5D=&columns%5B16%5D%5Bsearchable%5D=true&columns%5B16%5D%5Borderable%5D=false&columns%5B16%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B16%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=500&search%5BTERM%5D=28924&search%5BLEVEL_ID%5D=&search%5BCLASS_ID%5D=&search%5BCLASS_GROUP_ID%5D=&search%5BPHOTO%5D=&search%5BCARD%5D=&search%5Bkeyword%5D=&search%5BSTUDENT_STATUS%5D=%E0%B8%81%E0%B8%B3%E0%B8%A5%E0%B8%B1%E0%B8%87%E0%B8%A8%E0%B8%B6%E0%B8%81%E0%B8%A9%E0%B8%B2&search%5BORDER_BY%5D=1&rp=500&page=1&orders%5Bcolumn%5D=_checkbox&orders%5Bdir%5D=asc"


fetch_all_students() 
fetch_and_save(teacher_url, teacher_referer, teacher_body, "teacher_raw_data.json")  # โหลด teacher

