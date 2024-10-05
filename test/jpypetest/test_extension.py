# *****************************************************************************
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   See NOTICE file for details.
#
# *****************************************************************************
import common
import jpype
from jpype._jclass import *
from jpype.types import *
from jpype.imports import *
import inspect


class JExtensionTestCase(common.JPypeTestCase):

    def setUp(self):
        common.JPypeTestCase.setUp(self)

    def testExtendObject(self):
        from java.lang import Object
        class MyObject(Object):

            @JPublic
            def __init__(self):
                ...

        self.assertIsInstance(MyObject(), MyObject)

    def testAddedMethod(self):
        from java.lang import Object
        class MyObject(Object):

            @JPublic
            def __init__(self):
                ...

            @JPublic
            def func(self) -> JObject:
                return self

        o = MyObject()
        self.assertEqual(o.func(), o)

    def testInitOnce(self):
        TestBase = JClass("jpype.extension.TestBase")
        class MyObject(TestBase):

            def __init__(self):
                super().__init__()
                self.initCount += 1

            @JPublic
            def __init__(self):
                # FIXME damn super() is broke in the callbacks
                # even when it is a bound method it is broken
                super(TestBase, self).__init__()
                self.initCount += 1

        o = MyObject()
        # once in TestBase constructor, then in the __init__ callback from constructor
        # then again when the Python __init__ is called
        self.assertEqual(o.initCount, 3)

    def testOverrideSimple(self):
        from java.lang import Object, String
        class MyObject(Object):

            @JPublic
            def __init__(self):
                ...

            @JPublic
            @JOverride
            def toString(self) -> String:
                return "test"

        self.assertEqual(str(MyObject()), "test")

    def testOverloads(self):
        mode = -1

        class MyObject(JClass("jpype.extension.TestBase")):

            def __init__(self, *args, **kwargs):
                pass

            @JPublic
            def __init__(self):
                nonlocal mode
                mode = 0

            @JPublic
            def __init__(self, i: JInt):
                nonlocal mode
                mode = 1

            @JPublic
            def __init__(self, o: JObject):
                nonlocal mode
                mode = 2

            @JPublic
            @JOverride
            def identity(self, i: JInt) -> JInt:
                return 0

            @JPublic
            @JOverride
            def identity(self, o: JObject) -> JObject:
                return None

            @JPublic
            def func(self) -> JObject:
                return self

        o = MyObject()
        self.assertEqual(mode, 0)
        MyObject(JInt(1))
        self.assertEqual(mode, 1)
        MyObject(JObject())
        self.assertEqual(mode, 2)
        self.assertEqual(o.identity(JInt(1)), 0)
        self.assertEqual(o.identity(JObject()), None)

    def testSupercall(self):
        TestBase = JClass("jpype.extension.TestBase")
        class MyObject(TestBase):

            @JPublic
            def __init__(self):
                pass

            @JPublic
            @JOverride
            def identity(self, o: JObject) -> JObject:
                return None

            @JPublic
            def super_identity(self, o: JObject) -> JObject:
                return super().identity(o)

            def test_identity(self, o: JObject) -> JObject:
                return super().identity(o)

            def test_identity_explicit(self, o: JObject) -> JObject:
                return super(TestBase, self).identity(o)

            def get_super(self):
                return super()

            def get_explicit_super(self):
                return super(TestBase, self)

        o = MyObject()
        value = o.get_super()
        explicit = o.get_explicit_super()
        print(value)
        print(explicit)
        sentinel = JObject()
        # NOTE: when the java object comes back it gets a new python object
        # this will cause 'is' to fail so assertEqual is used instead
        self.assertEqual(o.test_identity(sentinel), sentinel)
        self.assertEqual(o.super_identity(sentinel), sentinel)


    def testPythonMembers(self):
        class MyObject(JClass("jpype.extension.TestBase")):

            def __init__(self):
                self.a = 0
                self.b = 1

            @JPublic
            def __init__(self):
                ...

            def inc(self):
                # FIXME test results don't show if it throws
                #self.index += 1
                pass
        o = MyObject()
        self.assertEqual(o.a, 0)
        self.assertEqual(o.b, 1)

    def testProtectedField(self):
        class MyObject(JClass("jpype.extension.TestBase")):

            @JPublic
            def __init__(self):
                ...

            def inc(self):
                # FIXME test results don't show if it throws
                #self.index += 1
                pass

        o = MyObject()
        o.inc()