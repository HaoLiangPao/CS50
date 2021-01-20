-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Evidence we know:
-- Time: July 28, 2020
-- Location: Chamberlin Street


-- 1. Get an idea of the overall infostructure of the database: .schema

-- 1. Get an idea of the crime records
SELECT * FROM crime_scene_reports LIMIT 10;
SELECT * FROM crime_scene_reports WHERE year = 2020 AND month = 7 AND day = 28 AND street = "Chamberlin Street";
-- id | year | month | day | street | description
-- 295 | 2020 | 7 | 28 | Chamberlin Street | Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.

-- 2. Find interviews of three witnesses
SELECT * FROM interviews WHERE year = 2020 AND month = 7 AND day = 28; -- check all records
-- id | name | year | month | day | transcript
-- 161 | Ruth | 2020 | 7 | 28 | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
-- 162 | Eugene | 2020 | 7 | 28 | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
-- 163 | Raymond | 2020 | 7 | 28 | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- 3. Check security logs of courthouse since all three witnesses have mentioned it
SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10; -- checked
SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25; -- check 10 minutes after 10:15 and after with the same license plate
SELECT * FROM
 (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour <= 10 AND minute < 25) AS recordA
  JOIN
 (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25) AS recordB
  ON recordA.license_plate = recordB.license_plate
WHERE
 recordA.activity = "entrance" AND recordB.activity = "exit"
; -- the theft should come in and out the courthouse within one day, so we have checked the cars arrived and left within the possible window
-- id | year | month | day | hour | minute | activity | license_plate | id | year | month | day | hour | minute | activity | license_plate
-- 231 | 2020 | 7 | 28 | 8 | 18 | entrance | L93JTIZ | 265 | 2020 | 7 | 28 | 10 | 21 | exit | L93JTIZ
-- 232 | 2020 | 7 | 28 | 8 | 23 | entrance | 94KL13X | 261 | 2020 | 7 | 28 | 10 | 18 | exit | 94KL13X
-- 254 | 2020 | 7 | 28 | 9 | 14 | entrance | 4328GD8 | 263 | 2020 | 7 | 28 | 10 | 19 | exit | 4328GD8
-- 255 | 2020 | 7 | 28 | 9 | 15 | entrance | 5P2BI95 | 260 | 2020 | 7 | 28 | 10 | 16 | exit | 5P2BI95
-- 256 | 2020 | 7 | 28 | 9 | 20 | entrance | 6P58WS2 | 262 | 2020 | 7 | 28 | 10 | 18 | exit | 6P58WS2


-- 4. Check ATM records finding out who get money out from Fifer Street this morning
SELECT * FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street"; -- get all withdraw records this morning
SELECT * FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street"); -- From the account id, get a list of possible people
-- account_number | person_id | creation_year
-- 49610011 | 686048 | 2010
-- 86363979 | 948985 | 2010
-- 26013199 | 514354 | 2012
-- 16153065 | 458378 | 2012
-- 28296815 | 395717 | 2014
-- 25506511 | 396669 | 2014
-- 28500762 | 467400 | 2014
-- 76054385 | 449774 | 2015
-- 81061156 | 438727 | 2018

-- 5. Use plate number and people id trying to filter a step more on possible people list
SELECT * FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
    (SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street"))
AND license_plate IN
(SELECT recordA.license_plate FROM
 (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour <= 10 AND minute < 25) AS recordA
  JOIN
 (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25) AS recordB
  ON recordA.license_plate = recordB.license_plate
WHERE
 recordA.activity = "entrance" AND recordB.activity = "exit");
-- id | name | phone_number | passport_number | license_plate
-- 396669 | Elizabeth | (829) 555-5269 | 7049073643 | L93JTIZ
-- 467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X

-- 6. Check phone calls made among these three
SELECT * FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28; -- Get all call records on the day of crime
SELECT * FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND caller IN
    (SELECT phone_number FROM people WHERE id IN
        (SELECT person_id FROM bank_accounts
            WHERE account_number IN
                (SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street"))
        AND license_plate IN
            (SELECT recordA.license_plate FROM
             (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour <= 10 AND minute < 25) AS recordA
              JOIN
             (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25) AS recordB
              ON recordA.license_plate = recordB.license_plate
            WHERE
             recordA.activity = "entrance" AND recordB.activity = "exit")
    );

-- only one number among all the possible numbers have fit all requirements, will find the theft
-- id | caller | receiver | year | month | day | duration
-- 233 | (367) 555-5533 | (375) 555-8161 | 2020 | 7 | 28 | 45
-- 236 | (367) 555-5533 | (344) 555-9601 | 2020 | 7 | 28 | 120
-- 245 | (367) 555-5533 | (022) 555-4052 | 2020 | 7 | 28 | 241
-- 285 | (367) 555-5533 | (704) 555-5790 | 2020 | 7 | 28 | 75
SELECT * FROM people WHERE phone_number = "(367) 555-5533";
-- id | name | phone_number | passport_number | license_plate
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X

-- 7. Based on the receiver numbers, check possible teammates
SELECT * FROM people WHERE phone_number IN
    (SELECT receiver FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND caller IN
        (SELECT phone_number FROM people WHERE id IN
            (SELECT person_id FROM bank_accounts
                WHERE account_number IN
                    (SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street"))
            AND license_plate IN
                (SELECT recordA.license_plate FROM
                 (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour <= 10 AND minute < 25) AS recordA
                  JOIN
                 (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25) AS recordB
                  ON recordA.license_plate = recordB.license_plate
                WHERE
                 recordA.activity = "entrance" AND recordB.activity = "exit")
        )
    );
-- teammates should be someone within this list of 4 people
-- id | name | phone_number | passport_number | license_plate
-- 315221 | Gregory | (022) 555-4052 | 3355598951 | V4C670D
-- 652398 | Carl | (704) 555-5790 | 7771405611 | 81MZ921
-- 864400 | Berthold | (375) 555-8161 |  | 4V16VO0
-- 985497 | Deborah | (344) 555-9601 | 8714200946 | 10I5658

-- 8. Find the flight they booked together
SELECT * FROM airports WHERE city = "Fiftyville"; -- get the id of the airport
-- id | abbreviation | full_name | city
-- 8 | CSF | Fiftyville Regional Airport | Fiftyville
SELECT * FROM flights WHERE
    origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2020 AND month = 7 AND day >= 28 AND day < 30;
SELECT * FROM flights WHERE
    origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2020 AND month = 7 AND day = 29;
-- id | origin_airport_id | destination_airport_id | year | month | day | hour | minute
-- 18 | 8 | 6 | 2020 | 7 | 29 | 16 | 0
-- 23 | 8 | 11 | 2020 | 7 | 29 | 12 | 15
-- 36 | 8 | 4 | 2020 | 7 | 29 | 8 | 20
-- 43 | 8 | 1 | 2020 | 7 | 29 | 9 | 30
-- 53 | 8 | 9 | 2020 | 7 | 29 | 15 | 20
SELECT * FROM passengers WHERE flight_id IN
    (SELECT id FROM flights WHERE
        origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2020 AND month = 7 AND day = 29); -- Get all passport_number of the passengers who is on all possible flights
-- flight_id | passport_number | seat
-- 18 | 2835165196 | 9C
-- 18 | 6131360461 | 2C
-- 18 | 3231999695 | 3C
-- 18 | 3592750733 | 4C
-- 18 | 2626335085 | 5D
-- 18 | 6117294637 | 6B
-- 18 | 2996517496 | 7A
-- 18 | 3915621712 | 8D
-- 23 | 4149859587 | 7D
-- 23 | 9183348466 | 8A
-- 23 | 7378796210 | 9B
-- 23 | 7874488539 | 2C
-- 23 | 4195341387 | 3A
-- 23 | 6263461050 | 4A
-- 23 | 3231999695 | 5A
-- 23 | 7951366683 | 6B
-- 36 | 7214083635 | 2A
-- 36 | 1695452385 | 3B
-- 36 | 5773159633 | 4A
-- 36 | 1540955065 | 5C
-- 36 | 8294398571 | 6C
-- 36 | 1988161715 | 6D
-- 36 | 9878712108 | 7A
-- 36 | 8496433585 | 7B
-- 43 | 7597790505 | 7B
-- 43 | 6128131458 | 8A
-- 43 | 6264773605 | 9A
-- 43 | 3642612721 | 2C
-- 43 | 4356447308 | 3B
-- 43 | 7441135547 | 4A
-- 53 | 7894166154 | 9B
-- 53 | 6034823042 | 2C
-- 53 | 4408372428 | 3D
-- 53 | 2312901747 | 4D
-- 53 | 1151340634 | 5A
-- 53 | 8174538026 | 6D
-- 53 | 1050247273 | 7A
-- 53 | 7834357192 | 8C


-- 9. Check people info table with the passport number list

SELECT listA.passport_number FROM
    (SELECT passport_number FROM passengers WHERE flight_id IN
        (SELECT id FROM flights WHERE
            origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2020 AND month = 7 AND day = 29)
    ) AS listA
        JOIN
    (SELECT * FROM people WHERE phone_number IN
        (SELECT receiver FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND caller IN
            (SELECT phone_number FROM people WHERE id IN
                (SELECT person_id FROM bank_accounts
                    WHERE account_number IN
                        (SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street"))
                AND license_plate IN
                    (SELECT recordA.license_plate FROM
                     (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour <= 10 AND minute < 25) AS recordA
                      JOIN
                     (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25) AS recordB
                      ON recordA.license_plate = recordB.license_plate
                    WHERE
                     recordA.activity = "entrance" AND recordB.activity = "exit")
            )
        )
    ) AS listB
        ON listA.passport_number = listB.passport_number
    ; -- No records, could be the one with no records, but will reduce the length of the list again to double check

-- teammates should be someone within this list of 4 people
-- id | name | phone_number | passport_number | license_plate
-- 315221 | Gregory | (022) 555-4052 | 3355598951 | V4C670D
-- 652398 | Carl | (704) 555-5790 | 7771405611 | 81MZ921
-- 864400 | Berthold | (375) 555-8161 |  | 4V16VO0
-- 985497 | Deborah | (344) 555-9601 | 8714200946 | 10I5658
SELECT * FROM
    (SELECT * FROM passengers WHERE flight_id IN
        (SELECT id FROM flights WHERE
            origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2020 AND month = 7 AND day = 29))
    WHERE
        passport_number = 5773159633; -- Get the flight id of the theft, will filter only the passengers from that flight, and the destination of the flight
-- flight_id | passport_number | seat
-- 36 | 5773159633 | 4A
SELECT * FROM passengers WHERE flight_id IN
        (SELECT id FROM flights WHERE
            origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") AND year = 2020 AND month = 7 AND day = 29 AND flight_id = 36);
-- flight_id | passport_number | seat
-- 36 | 7214083635 | 2A
-- 36 | 1695452385 | 3B
-- 36 | 5773159633 | 4A
-- 36 | 1540955065 | 5C
-- 36 | 8294398571 | 6C
-- 36 | 1988161715 | 6D
-- 36 | 9878712108 | 7A
-- 36 | 8496433585 | 7B


SELECT listA.passport_number FROM
    (SELECT passport_number FROM passengers WHERE flight_id = 36)
    AS listA
        JOIN
    (SELECT * FROM people WHERE phone_number IN
        (SELECT receiver FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND caller IN
            (SELECT phone_number FROM people WHERE id IN
                (SELECT person_id FROM bank_accounts
                    WHERE account_number IN
                        (SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street"))
                AND license_plate IN
                    (SELECT recordA.license_plate FROM
                     (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour <= 10 AND minute < 25) AS recordA
                      JOIN
                     (SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25) AS recordB
                      ON recordA.license_plate = recordB.license_plate
                    WHERE
                     recordA.activity = "entrance" AND recordB.activity = "exit")
            )
        )
    ) AS listB
        ON listA.passport_number = listB.passport_number
    ; -- No records again, which means the teammates' pssport_number is not recorded in the people table

-- 10. Get destination of the flight
SELECT * FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE id = 36);
-- id | abbreviation | full_name | city
-- 4 | LHR | Heathrow Airport | London