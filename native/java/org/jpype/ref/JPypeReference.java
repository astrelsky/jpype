/* ****************************************************************************
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  See NOTICE file for details.
**************************************************************************** */
package org.jpype.ref;

import java.lang.ref.PhantomReference;
import java.lang.ref.ReferenceQueue;

/**
 * (internal) Reference to a PyObject*.
 */
class JPypeReference extends PhantomReference<Object>
{

  long hostReference;
  long cleanup;
  int pool;
  int index;

  public JPypeReference(ReferenceQueue<Object> arg1, Object javaObject, long host, long cleanup)
  {
    super(javaObject, arg1);
    this.hostReference = host;
    this.cleanup = cleanup;
  }

  @Override
  public int hashCode()
  {
    return (int) hostReference;
  }

  @Override
  public boolean equals(Object arg0)
  {
    if (!(arg0 instanceof JPypeReference))
    {
      return false;
    }

    return ((JPypeReference) arg0).hostReference == hostReference;
  }
}
